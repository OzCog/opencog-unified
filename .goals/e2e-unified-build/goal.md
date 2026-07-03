# Goal: E2E Unified Build Sequence

## User Request

Create a single end-to-end build orchestrator script that unifies the fragmented build
pipeline (integrate-components.sh, build.sh, validate-integration.py, 14 test-phase scripts)
into one phase-aware command that builds the entire OpenCog cognitive architecture in
correct dependency order with validation at each stage.

## Refined Goal

Create `build-e2e.sh` — a single entry-point orchestrator that chains the complete
build lifecycle: prerequisite validation → component presence verification → phase-sequenced
CMake builds (respecting the cogutil→atomspace→cogserver→extensions→logic→cognitive→advanced→language→integration
dependency chain) → per-phase test execution → integration validation → structured build report.
The script must compose existing tools (build.sh for cmake/make, validate-integration.py for
structure checks, test-phase-*.sh scripts for testing) rather than duplicating their logic,
and must be aware of `component-config.json` for dependency ordering.

## Acceptance Criteria

- [ ] Running `./build-e2e.sh` from repo root produces a fully built system with all present components compiled in dependency order
- [ ] The script reads `component-config.json` to determine phase ordering and component dependencies
- [ ] Each phase (0-5) is built sequentially; a phase failure halts the pipeline with clear diagnostics showing which component/phase failed and why
- [ ] After each phase builds successfully, the corresponding test-phase script (if it exists) is executed
- [ ] `validate-integration.py` is invoked after all phases complete to confirm structural integrity
- [ ] A structured build report is written to `build-reports/latest.json` containing: phases attempted, components built, test results per phase, total time, pass/fail status
- [ ] A human-readable summary is printed to stdout at completion
- [ ] Supports `--phase N` flag to build only through phase N (inclusive of dependencies)
- [ ] Supports `--clean` flag to remove build artifacts before starting
- [ ] Supports `--skip-tests` flag to build without running test scripts
- [ ] Exit code 0 means all attempted phases built and tested successfully; non-zero indicates the specific failure point
- [ ] Script follows project shell conventions: `set -euo pipefail`, color output, function-based structure
- [ ] Script is executable and has proper shebang (`#!/bin/bash`)
- [ ] Does NOT duplicate logic from `build.sh` — delegates to it or uses cmake directly for the build step

## Scope Boundaries

**In scope:**
- The `build-e2e.sh` orchestrator script
- A `build-reports/` directory with JSON report output
- Integration with existing scripts (build.sh, validate-integration.py, test-phase-*.sh)
- Reading component-config.json for dependency/phase info
- Command-line flag parsing (--phase, --clean, --skip-tests, --help)
- Proper error handling and early-exit on failure

**Out of scope:**
- Modifying existing scripts (build.sh, validate-integration.py, test scripts)
- Cloning components from GitHub (that's integrate-components.sh's job)
- Docker image building
- CI/CD workflow changes (.github/workflows/)
- Cross-platform (Windows/macOS) support — Linux only
- Installing system dependencies (apt-get)
- Modifying CMakeLists.txt or any C++ source code

## Applicable Project Conventions

**Quality gate command:**
- `./validate-integration.py` (structural validation)
- `bash -n build-e2e.sh` (syntax check)
- `shellcheck build-e2e.sh` (if available)

**Commit convention:**
- Conventional commits: `type(scope): description`
- Role markers: `[B]` for Builder, `[I]` for Inspector
- Trailer: `Assisted-by: Claude:Sonnet-4.6` (Builder) / `Claude:Haiku-4.5` (Inspector)
- Title ≤72 characters, imperative mood

**Guidelines:**
- `.github/instructions/shell.instructions.md` — shell best practices (set -euo pipefail, functions, jq for JSON)
- `.github/instructions/opencog-unified.instructions.md` — project conventions and component dependencies

**Rules:**
- Never cancel long-running builds (timeouts must be generous)
- Follow component dependency order: cogutil → atomspace → cogserver → extensions → logic → cognitive → advanced → language → integration
- Build times: 30-60 minutes full build is normal
- Use `nproc` for parallel jobs
- Existing `build.sh` supports: BUILD_TYPE, BUILD_DIR, PARALLEL_JOBS, USE_CCACHE, USE_NINJA env vars

## Technical Context

**Existing infrastructure to compose:**
- `build.sh` — handles cmake configure + build + test for flat builds (env-var configured)
- `component-config.json` — defines all 17 components with: status, layer, phase, priority, dependencies[], build_requirements
- `validate-integration.py` — Python validator checking structure, dependencies, cmake integration
- `test-phase-ii.sh` through `test-phase-vi-comprehensive.sh` — 14 test scripts covering phases 2-6
- Root `CMakeLists.txt` — conditionally includes components via `if(EXISTS ...)` pattern

**Component layout:**
- Root-level: cogutil/, atomspace/, cogserver/, attention/, spacetime/, pln/, unify/, ure/, moses/
- components/ subdirectory: core/atomspace-rocks/, core/atomspace-restful/
- component-config.json tracks which are "present" vs "pending"

**Key constraint:** Only build components whose directories actually exist on disk (the script must gracefully handle partial installations where some components are "pending" in config but not yet cloned).
