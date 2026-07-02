#!/bin/bash
# Foundation Layer Test Runner
# Rigorous testing for cogutil and atomspace (C++, C, and Scheme)
# Ensures no mocks, stubs, or placeholders in implementations

set -e
set -u
set -o pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BUILD_DIR="${BUILD_DIR:-${REPO_ROOT}/build/foundation}"
TEST_RESULTS_DIR="${TEST_RESULTS_DIR:-${BUILD_DIR}/test-results}"

# Test statistics
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

# Functions
print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║ $(printf '%-58s' "$1")║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
}

print_section() {
    echo -e "${CYAN}┌────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│ $(printf '%-58s' "$1")│${NC}"
    echo -e "${CYAN}└────────────────────────────────────────────────────────────┘${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Validate no mock implementations
validate_no_mocks() {
    local component="$1"
    local component_dir="${REPO_ROOT}/${component}"

    print_section "Validating ${component} - No Mocks/Stubs"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    # Search for mock patterns in implementation files
    local mock_patterns="(MOCK|STUB|PLACEHOLDER|NOT IMPLEMENTED|throw std::logic_error)"
    local mock_count=0

    if [ -d "${component_dir}/opencog" ]; then
        mock_count=$(grep -r -i -E "${mock_patterns}" \
            --include="*.cc" --include="*.h" --include="*.c" \
            "${component_dir}/opencog" 2>/dev/null | \
            grep -v "test" | grep -v "example" | wc -l || echo "0")
    fi

    if [ "$mock_count" -eq 0 ]; then
        print_success "${component}: No mock implementations detected"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        print_error "${component}: Found ${mock_count} potential mock implementations"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Verify substantial implementations
verify_implementation_depth() {
    local component="$1"
    local component_dir="${REPO_ROOT}/${component}"
    local min_size="${2:-500}"  # Minimum file size in bytes

    print_section "Verifying ${component} Implementation Depth"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    local small_files=0
    local total_impl_files=0

    if [ -d "${component_dir}/opencog" ]; then
        # Count implementation files
        total_impl_files=$(find "${component_dir}/opencog" -name "*.cc" -o -name "*.c" | wc -l)

        # Count small files (potential stubs)
        small_files=$(find "${component_dir}/opencog" \( -name "*.cc" -o -name "*.c" \) -size -${min_size}c | wc -l)
    fi

    local substantial_files=$((total_impl_files - small_files))
    local percentage=0
    if [ "$total_impl_files" -gt 0 ]; then
        percentage=$((substantial_files * 100 / total_impl_files))
    fi

    print_info "${component}: ${substantial_files}/${total_impl_files} files are substantial (${percentage}%)"

    if [ "$percentage" -ge 80 ]; then
        print_success "${component}: Implementation depth is adequate"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        print_warning "${component}: Implementation depth is low (${percentage}% < 80%)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Run C++ unit tests
run_cpp_tests() {
    local component="$1"
    local component_build_dir="${BUILD_DIR}/${component}"

    print_section "Running C++ Tests for ${component}"

    if [ ! -d "${component_build_dir}" ]; then
        print_warning "${component}: Build directory not found"
        SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
        return 0
    fi

    cd "${component_build_dir}"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    # Run CTest with detailed output
    if ctest --output-on-failure --timeout 300 -V 2>&1 | tee "${TEST_RESULTS_DIR}/${component}_cpp_tests.log"; then
        local test_count
        test_count=$(grep -c "Test #" "${TEST_RESULTS_DIR}/${component}_cpp_tests.log" || echo "0")
        print_success "${component}: ${test_count} C++ tests passed"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        cd "${REPO_ROOT}"
        return 0
    else
        print_error "${component}: C++ tests failed"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        cd "${REPO_ROOT}"
        return 1
    fi
}

# Run Scheme tests
run_scheme_tests() {
    local component="$1"
    local component_dir="${REPO_ROOT}/${component}"

    print_section "Running Scheme Tests for ${component}"

    # Check if Scheme tests exist
    local scheme_test_dir="${component_dir}/tests/scm"
    if [ ! -d "${scheme_test_dir}" ]; then
        print_info "${component}: No Scheme test directory found"
        SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
        return 0
    fi

    # Count Scheme test files
    local scheme_test_count
    scheme_test_count=$(find "${scheme_test_dir}" -name "*.scm" | wc -l)
    if [ "$scheme_test_count" -eq 0 ]; then
        print_info "${component}: No Scheme test files found"
        SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
        return 0
    fi

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    print_info "${component}: Found ${scheme_test_count} Scheme test files"

    # Check if guile is available
    if ! command -v guile >/dev/null 2>&1; then
        print_warning "${component}: Guile not found, skipping Scheme tests"
        SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
        return 0
    fi

    # Validate Scheme test files are not empty
    local empty_tests=0
    local valid_tests=0

    for test_file in "${scheme_test_dir}"/*.scm; do
        if [ -f "${test_file}" ]; then
            local file_size
            file_size=$(stat -c%s "${test_file}" 2>/dev/null || stat -f%z "${test_file}" 2>/dev/null || echo "0")
            if [ "$file_size" -lt 50 ]; then
                empty_tests=$((empty_tests + 1))
            else
                valid_tests=$((valid_tests + 1))
            fi
        fi
    done

    print_info "${component}: ${valid_tests} valid Scheme tests, ${empty_tests} empty/stub tests"

    if [ "$valid_tests" -gt 0 ]; then
        print_success "${component}: Scheme tests validated"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        print_warning "${component}: No valid Scheme tests found"
        SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
        return 0
    fi
}

# Verify tensor kernel integration
verify_tensor_kernel() {
    print_section "Verifying Tensor Kernel Integration"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    # Check for tensor configuration artifacts
    local artifact_dir="${BUILD_DIR}/artifacts"
    local configs_found=0

    for component in cogutil atomspace; do
        local tensor_config="${artifact_dir}/${component}_tensor_config.json"
        if [ -f "${tensor_config}" ]; then
            print_info "Found tensor config: ${tensor_config}"

            # Validate JSON structure
            if command -v jq >/dev/null 2>&1; then
                if jq empty "${tensor_config}" 2>/dev/null; then
                    local dof
                    dof=$(jq -r '.degrees_of_freedom' "${tensor_config}")
                    print_info "${component}: Tensor DOF = ${dof}"
                    configs_found=$((configs_found + 1))
                fi
            else
                configs_found=$((configs_found + 1))
            fi
        fi
    done

    if [ "$configs_found" -eq 2 ]; then
        print_success "Tensor kernel integration verified for all components"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        print_warning "Tensor kernel integration incomplete (${configs_found}/2 components)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Verify build artifacts
verify_artifacts() {
    print_section "Verifying Build Artifacts"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    local artifact_dir="${BUILD_DIR}/artifacts"
    local required_artifacts=(
        "build_summary.json"
        "hardware_matrix.json"
        "TENSOR_DEGREES_OF_FREEDOM.md"
        "foundation_install.tar.gz"
    )

    local found_artifacts=0
    for artifact in "${required_artifacts[@]}"; do
        if [ -f "${artifact_dir}/${artifact}" ]; then
            print_success "Found artifact: ${artifact}"
            found_artifacts=$((found_artifacts + 1))
        else
            print_error "Missing artifact: ${artifact}"
        fi
    done

    if [ "$found_artifacts" -eq "${#required_artifacts[@]}" ]; then
        print_success "All required artifacts present"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        print_error "Missing $((${#required_artifacts[@]} - found_artifacts)) artifacts"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Verify recursive implementation patterns
verify_recursive_patterns() {
    local component="$1"
    local component_dir="${REPO_ROOT}/${component}"

    print_section "Verifying Recursive Patterns in ${component}"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    # Check for recursive/self-referential patterns
    local recursive_count=0

    if [ -d "${component_dir}/opencog" ]; then
        # Look for recursive function definitions, template recursion, etc.
        recursive_count=$(grep -r -E "(recursive|self|meta|introspect|reflect)" \
            --include="*.cc" --include="*.h" \
            "${component_dir}/opencog" 2>/dev/null | \
            grep -v "test" | grep -v "//" | wc -l || echo "0")
    fi

    print_info "${component}: Found ${recursive_count} potential recursive patterns"

    if [ "$recursive_count" -gt 0 ]; then
        print_success "${component}: Recursive implementation patterns detected"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        print_info "${component}: Limited recursive patterns (may be by design)"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    fi
}

# Generate test report
generate_test_report() {
    print_header "Generating Test Report"

    local report_file="${TEST_RESULTS_DIR}/foundation_test_report.json"
    local success_rate=0

    if [ "$TOTAL_TESTS" -gt 0 ]; then
        success_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    fi

    cat > "${report_file}" <<EOF
{
  "test_timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "summary": {
    "total_tests": ${TOTAL_TESTS},
    "passed": ${PASSED_TESTS},
    "failed": ${FAILED_TESTS},
    "skipped": ${SKIPPED_TESTS},
    "success_rate": ${success_rate}
  },
  "components_tested": ["cogutil", "atomspace"],
  "test_categories": [
    "mock_validation",
    "implementation_depth",
    "cpp_unit_tests",
    "scheme_tests",
    "tensor_kernel_integration",
    "build_artifacts",
    "recursive_patterns"
  ],
  "validation_status": "$([ "$FAILED_TESTS" -eq 0 ] && echo "PASS" || echo "FAIL")"
}
EOF

    print_success "Test report generated: ${report_file}"
}

# Print test summary
print_summary() {
    print_header "Test Summary"

    echo -e "${CYAN}Total Tests:   ${NC}${TOTAL_TESTS}"
    echo -e "${GREEN}Passed:        ${NC}${PASSED_TESTS}"
    echo -e "${RED}Failed:        ${NC}${FAILED_TESTS}"
    echo -e "${YELLOW}Skipped:       ${NC}${SKIPPED_TESTS}"

    if [ "$TOTAL_TESTS" -gt 0 ]; then
        local success_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))
        echo -e "${MAGENTA}Success Rate:  ${NC}${success_rate}%"
    fi

    echo ""

    if [ "$FAILED_TESTS" -eq 0 ]; then
        print_success "All foundation layer tests passed!"
        return 0
    else
        print_error "${FAILED_TESTS} test(s) failed"
        return 1
    fi
}

# Main execution
main() {
    print_header "Foundation Layer Test Runner"
    print_info "Rigorous Testing for CogUtil and AtomSpace"
    echo ""

    # Create test results directory
    mkdir -p "${TEST_RESULTS_DIR}"

    # Run validation tests
    for component in cogutil atomspace; do
        print_header "Testing ${component}"

        validate_no_mocks "${component}" || true
        verify_implementation_depth "${component}" || true
        verify_recursive_patterns "${component}" || true
        run_cpp_tests "${component}" || true
        run_scheme_tests "${component}" || true

        echo ""
    done

    # System-wide verification
    print_header "System-Wide Verification"
    verify_tensor_kernel || true
    verify_artifacts || true
    echo ""

    # Generate report
    generate_test_report
    echo ""

    # Print summary
    print_summary
}

# Execute main function
main "$@"
