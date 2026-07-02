#!/bin/bash
# Foundation Layer Integration Validation
# Validates all components are correctly set up without running full builds

set -e
set -u
set -o pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Functions
print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║ $(printf '%-58s' "$1")║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_file() {
    local file="$1"
    local description="$2"

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if [ -f "${file}" ]; then
        print_success "${description}"
        return 0
    else
        print_error "${description} - File not found: ${file}"
        return 1
    fi
}

check_executable() {
    local file="$1"
    local description="$2"

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if [ -x "${file}" ]; then
        print_success "${description}"
        return 0
    else
        print_error "${description} - Not executable: ${file}"
        return 1
    fi
}

check_directory() {
    local dir="$1"
    local description="$2"

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if [ -d "${dir}" ]; then
        print_success "${description}"
        return 0
    else
        print_error "${description} - Directory not found: ${dir}"
        return 1
    fi
}

validate_json() {
    local file="$1"
    local description="$2"

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if [ ! -f "${file}" ]; then
        print_error "${description} - File not found: ${file}"
        return 1
    fi

    # Check if jq is available for validation
    if command -v jq >/dev/null 2>&1; then
        if jq empty "${file}" 2>/dev/null; then
            print_success "${description}"
            return 0
        else
            print_error "${description} - Invalid JSON: ${file}"
            return 1
        fi
    else
        # Basic validation without jq
        if grep -q "{" "${file}" && grep -q "}" "${file}"; then
            print_success "${description} (basic check)"
            return 0
        else
            print_error "${description} - Malformed JSON: ${file}"
            return 1
        fi
    fi
}

# Main validation
main() {
    print_header "Foundation Layer Integration Validation"
    echo ""

    # Check foundation components exist
    print_header "Foundation Components"
    check_directory "${REPO_ROOT}/cogutil" "CogUtil component present"
    check_directory "${REPO_ROOT}/atomspace" "AtomSpace component present"
    echo ""

    # Check foundation scripts
    print_header "Foundation Scripts"
    check_executable "${REPO_ROOT}/scripts/foundation-seed-master.sh" "Master orchestrator"
    check_executable "${REPO_ROOT}/scripts/foundation-build.sh" "Build script"
    check_executable "${REPO_ROOT}/scripts/foundation-test.sh" "Test script"
    check_executable "${REPO_ROOT}/scripts/cognitive-kernel-seed.sh" "Kernel seed script"
    echo ""

    # Check cognitive kernel seed structure
    print_header "Cognitive Kernel Seed"
    check_directory "${REPO_ROOT}/cognitive-kernel-seed" "Kernel seed directory"
    check_directory "${REPO_ROOT}/cognitive-kernel-seed/config" "Config directory"
    check_directory "${REPO_ROOT}/cognitive-kernel-seed/loops" "Loops directory"
    check_directory "${REPO_ROOT}/cognitive-kernel-seed/introspection" "Introspection directory"
    echo ""

    # Check kernel configurations
    print_header "Kernel Configurations"
    validate_json "${REPO_ROOT}/cognitive-kernel-seed/config/kernel_seed.json" "Kernel seed config"
    validate_json "${REPO_ROOT}/cognitive-kernel-seed/config/meta_system.json" "Meta-system config"
    echo ""

    # Check meta-system loops
    print_header "Meta-System Loops"
    check_file "${REPO_ROOT}/cognitive-kernel-seed/loops/level0_object_processing.scm" "Level 0 (Object)"
    check_file "${REPO_ROOT}/cognitive-kernel-seed/loops/level1_meta_monitoring.scm" "Level 1 (Meta)"
    check_file "${REPO_ROOT}/cognitive-kernel-seed/loops/level2_introspection.scm" "Level 2 (Meta-Meta)"
    check_file "${REPO_ROOT}/cognitive-kernel-seed/loops/autognosis_init.scm" "Autognosis init"
    echo ""

    # Check introspection
    print_header "Introspection & Self-Image"
    check_file "${REPO_ROOT}/cognitive-kernel-seed/introspection/self_image_builder.scm" "Self-image builder"
    echo ""

    # Check documentation
    print_header "Documentation"
    check_file "${REPO_ROOT}/FOUNDATION_LAYER_GUIDE.md" "Foundation layer guide"
    check_file "${REPO_ROOT}/cognitive-kernel-seed/INTEGRATION_MANIFEST.md" "Integration manifest"
    check_file "${REPO_ROOT}/scripts/README.md" "Scripts README"
    echo ""

    # Validate Scheme syntax (basic check)
    print_header "Scheme Syntax Validation"
    local scheme_files=(
        "${REPO_ROOT}/cognitive-kernel-seed/loops/level0_object_processing.scm"
        "${REPO_ROOT}/cognitive-kernel-seed/loops/level1_meta_monitoring.scm"
        "${REPO_ROOT}/cognitive-kernel-seed/loops/level2_introspection.scm"
        "${REPO_ROOT}/cognitive-kernel-seed/loops/autognosis_init.scm"
        "${REPO_ROOT}/cognitive-kernel-seed/introspection/self_image_builder.scm"
    )

    for scm_file in "${scheme_files[@]}"; do
        TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

        # Basic syntax check: balanced parentheses
        local open_count

        open_count=$(grep -o "(" "${scm_file}" | wc -l)
        local close_count

        close_count=$(grep -o ")" "${scm_file}" | wc -l)

        if [ "$open_count" -eq "$close_count" ]; then
            print_success "$(basename ${scm_file}) - Balanced parentheses"
        else
            print_error "$(basename ${scm_file}) - Unbalanced parentheses ($open_count open, $close_count close)"
        fi
    done
    echo ""

    # Verify tensor configurations in kernel_seed.json
    print_header "Tensor Configuration Validation"
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if [ -f "${REPO_ROOT}/cognitive-kernel-seed/config/kernel_seed.json" ]; then
        if grep -q '"tensor_shape"' "${REPO_ROOT}/cognitive-kernel-seed/config/kernel_seed.json"; then
            print_success "Tensor shapes present in kernel config"
        else
            print_error "Tensor shapes missing from kernel config"
        fi
    fi

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ -f "${REPO_ROOT}/cognitive-kernel-seed/config/kernel_seed.json" ]; then
        if grep -q '"dof"' "${REPO_ROOT}/cognitive-kernel-seed/config/kernel_seed.json"; then
            print_success "Degrees of freedom present in kernel config"
        else
            print_error "Degrees of freedom missing from kernel config"
        fi
    fi
    echo ""

    # Check meta-loop configuration
    print_header "Meta-System Loop Configuration"
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if [ -f "${REPO_ROOT}/cognitive-kernel-seed/config/meta_system.json" ]; then
        if grep -q '"recursive_loops"' "${REPO_ROOT}/cognitive-kernel-seed/config/meta_system.json"; then
            print_success "Recursive loops configured"
        else
            print_error "Recursive loops missing from meta-system config"
        fi
    fi

    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ -f "${REPO_ROOT}/cognitive-kernel-seed/config/meta_system.json" ]; then
        if grep -q '"autognosis_parameters"' "${REPO_ROOT}/cognitive-kernel-seed/config/meta_system.json"; then
            print_success "Autognosis parameters configured"
        else
            print_error "Autognosis parameters missing"
        fi
    fi
    echo ""

    # Summary
    print_header "Validation Summary"
    echo -e "Total Checks:   ${TOTAL_CHECKS}"
    echo -e "${GREEN}Passed:         ${PASSED_CHECKS}${NC}"
    echo -e "${RED}Failed:         ${FAILED_CHECKS}${NC}"

    if [ "$FAILED_CHECKS" -eq 0 ]; then
        echo ""
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}   Foundation Layer Integration: VALIDATED ✓               ${NC}"
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        print_info "All foundation layer components are correctly set up"
        print_info "Ready for build and deployment"
        echo ""
        return 0
    else
        echo ""
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}   Foundation Layer Integration: FAILED ✗                  ${NC}"
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        print_error "${FAILED_CHECKS} check(s) failed - see errors above"
        echo ""
        return 1
    fi
}

# Execute
main "$@"
