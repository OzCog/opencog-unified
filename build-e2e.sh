#!/bin/bash
# ============================================================================
# build-e2e.sh — E2E Unified Build Orchestrator for OpenCog Unified
# ============================================================================
# Chains the complete build lifecycle:
#   prerequisite validation → component presence verification →
#   phase-sequenced CMake builds → per-phase test execution →
#   integration validation → structured build report
#
# Reads component-config.json for phase ordering and dependency info.
# Only builds components whose directories exist on disk.
# Delegates the actual cmake/make work to cmake directly (same pattern as
# build.sh) — does not duplicate that logic.
#
# Usage: ./build-e2e.sh [--phase N] [--clean] [--skip-tests] [--help]
# ============================================================================

set -euo pipefail

# ─── Script constants ─────────────────────────────────────────────────────────

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly CONFIG_FILE="${SCRIPT_DIR}/component-config.json"
readonly BUILD_REPORTS_DIR="${SCRIPT_DIR}/build-reports"
readonly REPORT_FILE="${BUILD_REPORTS_DIR}/latest.json"

# ─── Build configuration (mirrors build.sh env-var interface) ────────────────

BUILD_TYPE="${BUILD_TYPE:-Release}"
BUILD_DIR="${BUILD_DIR:-build}"
PARALLEL_JOBS="${PARALLEL_JOBS:-$(nproc)}"
USE_CCACHE="${USE_CCACHE:-ON}"
USE_NINJA="${USE_NINJA:-ON}"

# ─── Color output ─────────────────────────────────────────────────────────────

readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly BOLD='\033[1m'
readonly NC='\033[0m'

# ─── CLI flags ────────────────────────────────────────────────────────────────

MAX_PHASE=5
CLEAN=false
SKIP_TESTS=false

# ─── Timing ───────────────────────────────────────────────────────────────────

readonly BUILD_START_TIME="$(date +%s)"

# ─── Per-phase tracking (indexed arrays, populated at runtime) ────────────────

declare -A PHASE_COMPONENTS   # phase → space-separated full list from config
declare -A PHASE_PRESENT      # phase → space-separated subset present on disk
declare -A PHASE_BUILD_STATUS # phase → pass | fail | no_components | skipped
declare -A PHASE_TEST_STATUS  # phase → pass | fail | no_tests | skipped

# ─── Phase metadata ───────────────────────────────────────────────────────────

readonly -A PHASE_NAMES=(
    [0]="Foundation"
    [1]="Core Extensions"
    [2]="Logic Systems"
    [3]="Cognitive Systems"
    [4]="Advanced & Learning"
    [5]="Language & Integration"
)

# Primary test script to run after each phase's build (empty = none)
readonly -A PHASE_TEST_SCRIPTS=(
    [0]=""
    [1]=""
    [2]="test-phase-ii-logic-systems.sh"
    [3]="test-phase-iii-validation.sh"
    [4]="test-phase-iv-comprehensive.sh"
    [5]="test-phase-v-comprehensive.sh"
)

# Global build and validation status
BUILD_STATUS="unknown"
VALIDATE_STATUS="unknown"

# ─── Logging helpers ──────────────────────────────────────────────────────────

log_header() {
    echo ""
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${BOLD}${BLUE}  $1${NC}"
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════${NC}"
}

log_ok()   { echo -e "${GREEN}✅  $1${NC}"; }
log_err()  { echo -e "${RED}❌  $1${NC}" >&2; }
log_warn() { echo -e "${YELLOW}⚠️   $1${NC}"; }
log_info() { echo -e "${CYAN}ℹ️   $1${NC}"; }
log_step() { echo -e "${BOLD}▶   $1${NC}"; }

# ─── Usage ────────────────────────────────────────────────────────────────────

usage() {
    cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS]

E2E Unified Build Orchestrator for OpenCog Unified cognitive architecture.
Reads component-config.json for phase/dependency ordering, verifies which
components exist on disk, builds via CMake, runs phase tests, validates, and
writes a structured JSON report.

OPTIONS:
  --phase N      Build only through phase N inclusive (0-5, default: 5)
  --clean        Remove the build directory before starting
  --skip-tests   Build without running phase test scripts
  --help, -h     Show this help message

PHASES:
  0  Foundation         cogutil, atomspace, cogserver
  1  Core Extensions    atomspace-rocks, atomspace-restful, moses
  2  Logic Systems      unify, ure, language-learning
  3  Cognitive Systems  attention, spacetime
  4  Advanced           pln, miner, asmoses
  5  Language+Integr.   lg-atomese, learn, opencog

ENVIRONMENT VARIABLES (same as build.sh):
  BUILD_TYPE      Release|Debug          (default: Release)
  BUILD_DIR       Build directory path   (default: build)
  PARALLEL_JOBS   Parallel make/ninja    (default: nproc)
  USE_CCACHE      ON|OFF                 (default: ON)
  USE_NINJA       ON|OFF                 (default: ON)

REPORT:
  ${BUILD_REPORTS_DIR}/latest.json

EXAMPLES:
  ./build-e2e.sh                 # Full build, all phases
  ./build-e2e.sh --phase 3       # Build through phase 3
  ./build-e2e.sh --clean         # Wipe build dir then build
  ./build-e2e.sh --skip-tests    # Build without tests
  BUILD_TYPE=Debug ./build-e2e.sh --phase 0
EOF
}

# ─── Argument parsing ─────────────────────────────────────────────────────────

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --phase)
                [[ $# -ge 2 ]] || { log_err "--phase requires a numeric argument"; exit 1; }
                MAX_PHASE="$2"
                if [[ ! "${MAX_PHASE}" =~ ^[0-5]$ ]]; then
                    log_err "--phase must be 0–5, got: '${MAX_PHASE}'"
                    exit 1
                fi
                shift 2
                ;;
            --clean)
                CLEAN=true
                shift
                ;;
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --help|-h)
                usage
                exit 0
                ;;
            *)
                log_err "Unknown option: $1"
                usage >&2
                exit 1
                ;;
        esac
    done
}

# ─── Prerequisite check ───────────────────────────────────────────────────────

check_prerequisites() {
    log_header "Checking Prerequisites"

    local missing=()
    command -v cmake   >/dev/null 2>&1 || missing+=("cmake")
    command -v make    >/dev/null 2>&1 || missing+=("make")
    command -v jq      >/dev/null 2>&1 || missing+=("jq")
    command -v python3 >/dev/null 2>&1 || missing+=("python3")

    if [[ ${#missing[@]} -gt 0 ]]; then
        log_err "Missing required tools: ${missing[*]}"
        log_err "Install with: sudo apt-get install -y ${missing[*]}"
        exit 1
    fi

    [[ -f "${CONFIG_FILE}" ]] || {
        log_err "component-config.json not found: ${CONFIG_FILE}"
        exit 1
    }

    [[ -f "${SCRIPT_DIR}/validate-integration.py" ]] || {
        log_err "validate-integration.py not found in ${SCRIPT_DIR}"
        exit 1
    }

    if [[ "${USE_NINJA}" == "ON" ]]; then
        command -v ninja >/dev/null 2>&1 || log_warn "ninja not found — will fall back to Unix Makefiles"
    fi
    if [[ "${USE_CCACHE}" == "ON" ]]; then
        command -v ccache >/dev/null 2>&1 || log_warn "ccache not found — builds will not be cached"
    fi

    log_ok "Prerequisites satisfied"
}

# ─── Component discovery ──────────────────────────────────────────────────────

# Returns the list of component names for a given phase via stdout.
# Phase 0 is derived from integration_phase == 0 in the component definitions.
# Phases 1–5 come from integration_phases.phase_N.components[].
get_phase_components() {
    local phase="$1"
    if [[ "${phase}" -eq 0 ]]; then
        jq -r '
          .opencog_unified_components
          | to_entries[]
          | .value
          | to_entries[]
          | select(.value.integration_phase == 0)
          | .key
        ' "${CONFIG_FILE}" | sort
    else
        jq -r --argjson p "${phase}" \
          '.integration_phases["phase_\($p)"].components[]' \
          "${CONFIG_FILE}" 2>/dev/null || true
    fi
}

# Prints the absolute path of component on disk if it exists; returns 1 if not.
find_component_on_disk() {
    local component="$1"
    # Root-level directory (most OpenCog components live here)
    if [[ -d "${SCRIPT_DIR}/${component}" ]]; then
        echo "${SCRIPT_DIR}/${component}"
        return 0
    fi
    # components/ sub-tree (some storage backends live here)
    local subdir
    for subdir in core logic cognitive advanced learning language integration; do
        if [[ -d "${SCRIPT_DIR}/components/${subdir}/${component}" ]]; then
            echo "${SCRIPT_DIR}/components/${subdir}/${component}"
            return 0
        fi
    done
    return 1
}

# ─── Phase inventory ──────────────────────────────────────────────────────────

inventory_phases() {
    log_header "Component Inventory (Phases 0–${MAX_PHASE})"

    local phase comp present_list all_list n_all n_present

    for phase in $(seq 0 "${MAX_PHASE}"); do
        all_list="$(get_phase_components "${phase}" | tr '\n' ' ')"
        all_list="${all_list% }"   # strip trailing space
        present_list=""

        for comp in ${all_list}; do
            if find_component_on_disk "${comp}" >/dev/null 2>&1; then
                present_list="${present_list}${comp} "
            fi
        done
        present_list="${present_list% }"

        PHASE_COMPONENTS[${phase}]="${all_list}"
        PHASE_PRESENT[${phase}]="${present_list}"

        n_all=$(echo "${all_list}" | wc -w | tr -d '[:space:]')
        n_present=$(echo "${present_list}" | wc -w | tr -d '[:space:]')
        [[ -z "${all_list}" ]] && n_all=0
        [[ -z "${present_list}" ]] && n_present=0

        log_step "Phase ${phase} — ${PHASE_NAMES[${phase}]} (${n_present}/${n_all} present)"

        for comp in ${present_list}; do
            log_ok "  ${comp}"
        done

        for comp in ${all_list}; do
            if ! find_component_on_disk "${comp}" >/dev/null 2>&1; then
                log_warn "  ${comp} (pending — not on disk)"
            fi
        done
    done
}

# ─── Clean ────────────────────────────────────────────────────────────────────

do_clean() {
    log_header "Cleaning Build Artifacts"
    if [[ -d "${SCRIPT_DIR}/${BUILD_DIR}" ]]; then
        rm -rf "${SCRIPT_DIR:?}/${BUILD_DIR}"
        log_ok "Removed ${BUILD_DIR}/"
    else
        log_info "Nothing to clean (${BUILD_DIR}/ does not exist)"
    fi
}

# ─── CMake configure ──────────────────────────────────────────────────────────

configure_cmake() {
    log_header "CMake Configuration"

    local generator="Unix Makefiles"
    local extra_flags=()

    if [[ "${USE_NINJA}" == "ON" ]] && command -v ninja >/dev/null 2>&1; then
        generator="Ninja"
    fi
    if [[ "${USE_CCACHE}" == "ON" ]] && command -v ccache >/dev/null 2>&1; then
        extra_flags+=(
            "-DCMAKE_C_COMPILER_LAUNCHER=ccache"
            "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache"
        )
    fi

    log_info "Generator:     ${generator}"
    log_info "Build type:    ${BUILD_TYPE}"
    log_info "Parallel jobs: ${PARALLEL_JOBS}"
    log_info "Build dir:     ${BUILD_DIR}/"

    mkdir -p "${SCRIPT_DIR}/${BUILD_DIR}"

    cmake \
        -S "${SCRIPT_DIR}" \
        -B "${SCRIPT_DIR}/${BUILD_DIR}" \
        -G "${generator}" \
        -DCMAKE_BUILD_TYPE="${BUILD_TYPE}" \
        -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
        "${extra_flags[@]+"${extra_flags[@]}"}"

    log_ok "CMake configuration complete"
}

# ─── Phase build ──────────────────────────────────────────────────────────────
#
# The root CMakeLists.txt uses if(EXISTS ...) to conditionally add components
# in dependency order.  We invoke cmake --build once per phase to benefit from
# incremental builds: phase 0's targets are compiled first; phase 1 targets
# that depend on them find them already built; etc.  cmake itself enforces
# the internal dep graph, so subsequent phase builds are fast when deps are
# already up-to-date.

build_phase() {
    local phase="$1"
    local present="${PHASE_PRESENT[${phase}]:-}"

    if [[ -z "${present}" ]]; then
        log_warn "Phase ${phase} (${PHASE_NAMES[${phase}]}): no components on disk — skipping"
        PHASE_BUILD_STATUS[${phase}]="no_components"
        return 0
    fi

    local n_present
    n_present=$(echo "${present}" | wc -w | tr -d '[:space:]')
    log_step "Building phase ${phase} — ${PHASE_NAMES[${phase}]} (${n_present} present: ${present})"

    local phase_log="${BUILD_REPORTS_DIR}/build-phase${phase}.log"
    local phase_start
    phase_start="$(date +%s)"

    if cmake \
        --build "${SCRIPT_DIR}/${BUILD_DIR}" \
        --config "${BUILD_TYPE}" \
        -j "${PARALLEL_JOBS}" \
        2>&1 | tee "${phase_log}"; then
        local elapsed=$(( $(date +%s) - phase_start ))
        log_ok "Phase ${phase} build succeeded (${elapsed}s)"
        PHASE_BUILD_STATUS[${phase}]="pass"
    else
        local elapsed=$(( $(date +%s) - phase_start ))
        log_err "Phase ${phase} (${PHASE_NAMES[${phase}]}) build FAILED after ${elapsed}s"
        log_err "See log: ${phase_log}"
        PHASE_BUILD_STATUS[${phase}]="fail"
        BUILD_STATUS="fail"
        return 1
    fi
}

build_all_phases() {
    log_header "Build — Phases 0–${MAX_PHASE}"

    configure_cmake

    for phase in $(seq 0 "${MAX_PHASE}"); do
        build_phase "${phase}" || {
            BUILD_STATUS="fail"
            # Mark remaining phases as skipped in the report
            for remaining in $(seq $((phase + 1)) "${MAX_PHASE}"); do
                PHASE_BUILD_STATUS[${remaining}]="skipped"
                PHASE_TEST_STATUS[${remaining}]="skipped"
            done
            return 1
        }
    done

    BUILD_STATUS="pass"
    log_ok "All phases (0–${MAX_PHASE}) built successfully"
}

# ─── Phase tests ──────────────────────────────────────────────────────────────

run_phase_tests() {
    local phase="$1"
    local script_name="${PHASE_TEST_SCRIPTS[${phase}]:-}"

    if [[ -z "${script_name}" ]]; then
        PHASE_TEST_STATUS[${phase}]="no_tests"
        return 0
    fi

    local script_path="${SCRIPT_DIR}/${script_name}"
    if [[ ! -f "${script_path}" ]]; then
        log_warn "Phase ${phase} test script not found: ${script_name} — skipping"
        PHASE_TEST_STATUS[${phase}]="no_tests"
        return 0
    fi

    log_step "Running phase ${phase} tests: ${script_name}"
    local test_log="${BUILD_REPORTS_DIR}/test-phase${phase}.log"

    if bash "${script_path}" 2>&1 | tee "${test_log}"; then
        log_ok "Phase ${phase} tests passed"
        PHASE_TEST_STATUS[${phase}]="pass"
    else
        log_err "Phase ${phase} tests FAILED — see ${test_log}"
        PHASE_TEST_STATUS[${phase}]="fail"
        return 1
    fi
}

run_all_tests() {
    log_header "Phase Tests (0–${MAX_PHASE})"

    for phase in $(seq 0 "${MAX_PHASE}"); do
        local bs="${PHASE_BUILD_STATUS[${phase}]:-unknown}"
        if [[ "${bs}" == "pass" ]]; then
            run_phase_tests "${phase}" || return 1
        else
            log_info "Phase ${phase}: skipping tests (build status: ${bs})"
            PHASE_TEST_STATUS[${phase}]="skipped"
        fi
    done
}

# ─── Integration validation ───────────────────────────────────────────────────

run_validation() {
    log_header "Integration Validation"

    local val_log="${BUILD_REPORTS_DIR}/validation.log"

    # --no-build: we already built; skip validate-integration.py's cmake test
    if python3 "${SCRIPT_DIR}/validate-integration.py" --no-build 2>&1 | tee "${val_log}"; then
        log_ok "Integration validation passed"
        VALIDATE_STATUS="pass"
    else
        log_warn "Integration validation reported issues (non-fatal) — see ${val_log}"
        VALIDATE_STATUS="warn"
    fi
}

# ─── JSON report ──────────────────────────────────────────────────────────────

write_report() {
    mkdir -p "${BUILD_REPORTS_DIR}"

    local total_time=$(( $(date +%s) - BUILD_START_TIME ))
    local overall_status="pass"
    local phase phases_json=""
    local first=true

    for phase in $(seq 0 "${MAX_PHASE}"); do
        local bs="${PHASE_BUILD_STATUS[${phase}]:-unknown}"
        local ts="${PHASE_TEST_STATUS[${phase}]:-unknown}"
        [[ "${bs}" == "fail" || "${ts}" == "fail" ]] && overall_status="fail"

        # Build JSON arrays for components
        local comp_json present_json
        local comp_str="${PHASE_COMPONENTS[${phase}]:-}"
        local pres_str="${PHASE_PRESENT[${phase}]:-}"

        if [[ -n "${comp_str}" ]]; then
            comp_json="$(printf '%s' "${comp_str}" | \
                jq -Rc 'split(" ") | map(select(length > 0))')"
        else
            comp_json="[]"
        fi

        if [[ -n "${pres_str}" ]]; then
            present_json="$(printf '%s' "${pres_str}" | \
                jq -Rc 'split(" ") | map(select(length > 0))')"
        else
            present_json="[]"
        fi

        local phase_obj
        phase_obj="$(jq -n \
            --argjson phase "${phase}" \
            --arg name "${PHASE_NAMES[${phase}]:-Unknown}" \
            --arg build_status "${bs}" \
            --arg test_status  "${ts}" \
            --argjson components "${comp_json}" \
            --argjson present    "${present_json}" \
            '{
                phase: $phase,
                name: $name,
                build_status: $build_status,
                test_status: $test_status,
                components_defined: $components,
                components_present: $present
            }')"

        if [[ "${first}" == true ]]; then
            phases_json="${phase_obj}"
            first=false
        else
            phases_json="${phases_json},${phase_obj}"
        fi
    done

    jq -n \
        --arg  timestamp      "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        --argjson total_time  "${total_time}" \
        --argjson max_phase   "${MAX_PHASE}" \
        --arg  overall        "${overall_status}" \
        --arg  build          "${BUILD_STATUS}" \
        --arg  validation     "${VALIDATE_STATUS}" \
        --arg  skip_tests     "${SKIP_TESTS}" \
        --argjson phases      "[${phases_json}]" \
        '{
            timestamp:            $timestamp,
            total_time_seconds:   $total_time,
            max_phase_attempted:  $max_phase,
            overall_status:       $overall,
            build_status:         $build,
            validation_status:    $validation,
            tests_skipped:        ($skip_tests == "true"),
            phases:               $phases
        }' > "${REPORT_FILE}"

    log_ok "Report written → ${REPORT_FILE}"
}

# ─── Human-readable summary ───────────────────────────────────────────────────

print_summary() {
    local total_time=$(( $(date +%s) - BUILD_START_TIME ))
    local n_pass=0 n_fail=0 n_skip=0 overall_status="pass"
    local phase

    for phase in $(seq 0 "${MAX_PHASE}"); do
        case "${PHASE_BUILD_STATUS[${phase}]:-unknown}" in
            pass)           n_pass=$((n_pass + 1)) ;;
            fail)           n_fail=$((n_fail + 1)); overall_status="fail" ;;
            no_components)  n_skip=$((n_skip + 1)) ;;
            skipped)        n_skip=$((n_skip + 1)) ;;
        esac
        [[ "${PHASE_TEST_STATUS[${phase}]:-}" == "fail" ]] && overall_status="fail"
    done

    log_header "Build Summary"
    printf "  %-26s %s\n"  "Timestamp:"       "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf "  %-26s %ds\n" "Total time:"      "${total_time}"
    printf "  %-26s 0–%d\n" "Phases attempted:" "${MAX_PHASE}"
    printf "  %-26s %d\n"  "Phases built:"    "${n_pass}"
    printf "  %-26s %d\n"  "Phases failed:"   "${n_fail}"
    printf "  %-26s %d\n"  "Phases skipped:"  "${n_skip}"
    printf "  %-26s %s\n"  "Validation:"      "${VALIDATE_STATUS}"
    echo ""
    echo "  Phase-level results:"

    for phase in $(seq 0 "${MAX_PHASE}"); do
        local bs="${PHASE_BUILD_STATUS[${phase}]:-?}"
        local ts="${PHASE_TEST_STATUS[${phase}]:-?}"
        local icon

        case "${bs}" in
            pass)           icon="${GREEN}✅${NC}" ;;
            fail)           icon="${RED}❌${NC}" ;;
            no_components)  icon="${YELLOW}⚬${NC}" ;;
            skipped)        icon="${YELLOW}→${NC}" ;;
            *)              icon="  " ;;
        esac

        printf "  %b  Phase %d  %-22s build=%-14s tests=%s\n" \
            "${icon}" "${phase}" "(${PHASE_NAMES[${phase}]}):" "${bs}" "${ts}"
    done

    echo ""
    printf "  Report: %s\n" "${REPORT_FILE}"
    echo ""

    if [[ "${overall_status}" == "pass" ]]; then
        log_ok "E2E build completed successfully!"
        return 0
    else
        log_err "E2E build finished with FAILURES. See report and per-phase logs in ${BUILD_REPORTS_DIR}/"
        return 1
    fi
}

# ─── Main ─────────────────────────────────────────────────────────────────────

main() {
    parse_args "$@"

    mkdir -p "${BUILD_REPORTS_DIR}"

    log_header "OpenCog Unified — E2E Build Orchestrator"
    log_info "Timestamp:   $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    log_info "Max phase:   ${MAX_PHASE} (${PHASE_NAMES[${MAX_PHASE}]})"
    log_info "Build type:  ${BUILD_TYPE}"
    log_info "Clean:       ${CLEAN}"
    log_info "Skip tests:  ${SKIP_TESTS}"

    check_prerequisites

    [[ "${CLEAN}" == "true" ]] && do_clean

    inventory_phases

    build_all_phases

    if [[ "${SKIP_TESTS}" == "true" ]]; then
        log_info "Skipping phase tests (--skip-tests)"
        for phase in $(seq 0 "${MAX_PHASE}"); do
            PHASE_TEST_STATUS[${phase}]="skipped"
        done
    else
        run_all_tests
    fi

    run_validation

    write_report
    print_summary
}

main "$@"
