# OpenCog Unified Development Instructions

**CRITICAL:** Always follow these instructions first and fallback to additional search and context gathering only if the information here is incomplete or found to be in error.

## Working Effectively

### Repository Bootstrap and Dependencies
- Install system dependencies:
  ```bash
  # Ubuntu/Debian - Essential dependencies (REQUIRED)
  sudo apt-get update
  sudo apt-get install -y \
      cmake build-essential \
      libboost-all-dev \
      python3-dev \
      guile-2.2-dev \
      librocksdb-dev
  
  # Alternative for newer Ubuntu (if guile-2.2-dev unavailable)
  sudo apt-get install -y guile-3.0-dev
  ```

- Bootstrap build environment:
  ```bash
  mkdir -p build
  cd build
  cmake .. -DCMAKE_BUILD_TYPE=Release
  ```
  **TIMING:** CMake configuration takes ~6 seconds. Set timeout to 10+ minutes.

### Build Process
- **NEVER CANCEL builds or long-running commands. Build may take 45+ minutes.**
- Full system build:
  ```bash
  cd build
  make -j$(nproc)
  ```
  **TIMING:** Full build takes 30-60 minutes depending on components. **NEVER CANCEL.** Set timeout to 90+ minutes.

- Single-threaded verbose build (for troubleshooting):
  ```bash
  make -j1 VERBOSE=1
  ```
  **TIMING:** Single-threaded build takes 60-90 minutes. **NEVER CANCEL.** Set timeout to 120+ minutes.

### Component Integration and Testing
- Integrate all components (clones from GitHub):
  ```bash
  ./integrate-components.sh all
  ```
  **TIMING:** Component integration takes 15-30 minutes. **NEVER CANCEL.** Set timeout to 45+ minutes.

- Integrate specific phases:
  ```bash
  ./integrate-components.sh 1    # Phase 1: Core Extensions
  ./integrate-components.sh 2    # Phase 2: Logic Systems
  ./integrate-components.sh 3    # Phase 3: Cognitive Systems
  ./integrate-components.sh 4    # Phase 4: Advanced & Learning
  ./integrate-components.sh 5    # Phase 5: Language & Integration
  ```
  **TIMING:** Each phase takes 5-10 minutes. Set timeout to 20+ minutes per phase.

- Validate integration:
  ```bash
  ./validate-integration.py
  ```
  **TIMING:** Full validation takes 2-5 minutes. Set timeout to 15+ minutes.

- Validate specific phase:
  ```bash
  ./validate-integration.py --phase 1
  ```
  **TIMING:** Phase validation takes 30-60 seconds. Set timeout to 5+ minutes.

### Testing Strategy
- Run integration tests:
  ```bash
  cd tests/integration
  python3 -m pytest -v
  # If pytest unavailable, run directly:
  python3 test_moses.py
  python3 test_atomspace-rocks.py
  python3 test_atomspace-restful.py
  ```
  **TIMING:** Integration tests take 1-3 minutes total. Set timeout to 10+ minutes.

- Run comprehensive validation:
  ```bash
  ./tests/comprehensive-test-runner.sh
  ```
  **TIMING:** Comprehensive tests take 5-10 minutes. **NEVER CANCEL.** Set timeout to 20+ minutes.

- Run phase-specific tests:
  ```bash
  ./test-phase-ii-comprehensive.sh
  ./test-phase-iii-validation.sh
  ./test-phase-iv-comprehensive.sh
  ```
  **TIMING:** Each phase test takes 3-8 minutes. Set timeout to 15+ minutes each.

## Validation and Quality Assurance

### Manual Validation Requirements
**CRITICAL:** After making changes, ALWAYS run these validation scenarios:

1. **Build Validation Scenario:**
   ```bash
   # Clean rebuild to verify changes
   rm -rf build
   mkdir build && cd build
   cmake .. -DCMAKE_BUILD_TYPE=Debug
   make -j$(nproc)
   ```
   **Expected:** Build completes successfully. Check for new compilation errors.

2. **Integration Validation Scenario:**
   ```bash
   # Verify component integration
   ./validate-integration.py
   # Check specific components mentioned in your changes
   ./validate-integration.py --phase [relevant_phase]
   ```
   **Expected:** All validation checks pass. No missing dependencies.

3. **Component Testing Scenario:**
   ```bash
   # Test relevant components after changes
   cd tests/integration
   python3 test_[relevant_component].py
   ```
   **Expected:** All tests pass. No runtime errors.

### Critical Lint and Format Commands
- **ALWAYS** run before committing changes:
  ```bash
  # Check for placeholder implementations (must be clean)
  grep -r -i -E "(TODO|FIXME|STUB|MOCK|PLACEHOLDER|NOT IMPLEMENTED)" \
      --include="*.cc" --include="*.h" --include="*.scm" .
  
  # Verify substantial implementations (files > 500 bytes for .cc, > 200 bytes for .scm)
  find . -name "*.cc" -size -500c -exec echo "Warning: Small implementation {}" \;
  find . -name "*.scm" -size -200c -exec echo "Warning: Small implementation {}" \;
  ```

## Repository Structure and Navigation

### Key Components and Locations
- **Foundation Layer:** `cogutil/` - Core utilities (build first)
- **Core Layer:** `atomspace/` - Knowledge representation, `cogserver/` - Distributed server
- **Storage:** `atomspace-rocks/` - RocksDB backend, `atomspace-restful/` - REST API
- **Logic Layer:** `unify/` - Pattern matching, `ure/` - Unified Rule Engine  
- **Cognitive:** `attention/` - ECAN attention, `spacetime/` - Spatial-temporal reasoning
- **Advanced:** `pln/` - Probabilistic logic, `miner/` - Pattern mining, `asmoses/` - AtomSpace MOSES
- **Learning:** `moses/` - Evolutionary optimization
- **Language:** `lg-atomese/` - Link Grammar, `learn/` - Unsupervised learning, `language-learning/`
- **Integration:** `opencog/` - Main integration component

### Important Directories
- **Scripts:** Root directory contains integration and validation scripts
- **Tests:** `tests/integration/` - Component tests, `tests/` - Comprehensive test suites
- **Build:** `build/` - CMake build directory (create as needed)
- **Documentation:** `QUICK-START.md` - Development workflow, `DEVELOPMENT-ROADMAP.md` - Complete plan

### CMake Integration Pattern
All components follow this CMake pattern in root `CMakeLists.txt`:
```cmake
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/[component]/CMakeLists.txt")
    add_subdirectory([component])
endif()
```

## Dependency Management

### Component Dependencies (Critical for Development)
- **atomspace-rocks** depends on: atomspace
- **atomspace-restful** depends on: atomspace  
- **unify** depends on: atomspace
- **ure** depends on: atomspace, unify
- **attention** depends on: atomspace, cogserver
- **spacetime** depends on: atomspace
- **pln** depends on: atomspace, ure, spacetime
- **miner** depends on: atomspace, ure
- **moses** depends on: cogutil
- **asmoses** depends on: atomspace, ure
- **lg-atomese** depends on: atomspace
- **learn** depends on: atomspace, cogserver
- **language-learning** depends on: cogutil
- **opencog** depends on: atomspace, cogserver, attention, ure, lg-atomese

### Build Order Requirements
1. **Foundation:** cogutil
2. **Core:** atomspace, cogserver  
3. **Extensions:** atomspace-rocks, atomspace-restful
4. **Logic:** unify → ure
5. **Cognitive:** attention, spacetime
6. **Advanced:** pln, miner, asmoses
7. **Language:** lg-atomese, learn, language-learning
8. **Integration:** opencog

## Common Issues and Solutions

### Build Failures
- **Missing Boost:** Install `libboost-all-dev` - builds will fail without it
- **Missing Guile:** Install `guile-2.2-dev` or `guile-3.0-dev` - required for scheme bindings
- **CMake errors:** Check dependency order, ensure all required components are present
- **Clean rebuild:** `rm -rf build && mkdir build && cd build && cmake ..`

### Integration Issues  
- **Component missing:** Use `./integrate-components.sh [phase]` to clone from GitHub
- **Dependency errors:** Check `./validate-integration.py` output for missing components
- **Monorepo structure:** Components should NOT have `.git` directories (removed during integration)

### Validation Failures
- **Phase validation fails:** Check that all phase components are integrated and built
- **Test failures:** Verify Python environment, run tests individually to isolate issues
- **CMake integration issues:** Check that component is added to main CMakeLists.txt

## Quick Reference Commands

### Most Frequently Used Commands
```bash
# Quick status check (run first)
./validate-integration.py --no-build

# Full development cycle
./integrate-components.sh all
mkdir -p build && cd build && cmake ..
make -j$(nproc)          # NEVER CANCEL - 60+ min timeout
cd .. && ./validate-integration.py

# Rapid iteration for specific phase
./integrate-components.sh [1-5]
cd build && make -j$(nproc)  # NEVER CANCEL
./validate-integration.py --phase [1-5]

# Clean development restart
rm -rf build components/*/
./integrate-components.sh all
mkdir build && cd build && cmake .. && make -j$(nproc)
```

### Expected Output Validation
When commands work correctly, expect:
- **CMake configuration:** "Build type: Release" message, may show warnings about missing Boost/Guile  
- **Integration validation:** "Phase X validation passed" or "PARTIAL" status with specific error details
- **Python tests:** "Ran X tests in Y.YYYs" with "OK" status
- **Component integration:** 38+ validation results (SUCCESS/ERROR/WARNING messages)
- **Placeholder detection:** 700+ instances found (normal for this codebase)

### Debug and Troubleshooting Commands
```bash
# Verbose single-threaded build for errors
cd build && make -j1 VERBOSE=1

# Check component integration status
ls -la components/*/  # Should show folders without .git directories

# Manual test execution
cd tests/integration && python3 test_moses.py
```

## Development Workflow Best Practices

1. **Always start with:** `./validate-integration.py --no-build` to check current state
2. **Before making changes:** Ensure clean build with `make -j$(nproc)` (60+ min timeout)
3. **After making changes:** Run `./validate-integration.py` to verify integration
4. **Before committing:** Check for placeholders and run relevant phase tests
5. **For component work:** Focus on specific phases rather than full system rebuild
6. **For troubleshooting:** Use single-threaded verbose builds and individual component tests

**Remember:** This is a complex cognitive system with 14+ integrated components. Build times are long but necessary. Never cancel long-running operations - they will complete successfully with proper timeouts.

## AI Team Agents (Copilot Chat)

Invoke specialized personas with `@agent-name` in Copilot Chat:

| Agent | Persona | Use For |
|-------|---------|---------|
| `@nova-cpp` | Nova (Core Engineer) | C++ implementation, AtomSpace, CMake, builds |
| `@sage-scheme` | Sage (Logic Engineer) | Guile/Scheme, URE rules, PLN, pattern matching |
| `@milo-research` | Milo (Research Lead) | Algorithms, MOSES, attention dynamics, papers |
| `@kira-architect` | Kira (Architect) | System design, component interactions, AGI patterns |
| `@ivy-qa` | Ivy (QA Engineer) | Testing, validation, bug filing |
| `@remy-producer` | Remy (Producer) | Sprint planning, coordination, scope control |
| `@dash-devops` | Dash (DevOps) | CI/CD, Docker, build infrastructure |

## Instruction Stacking

Instructions auto-activate by file type:
- **All files**: `opencog-unified.instructions.md` (project context)
- **C++ files** (`.cc/.cpp/.h/.hpp`): + `opencog-cpp.instructions.md` + `cmake-vcpkg.instructions.md` + `cpp-language-service-tools.instructions.md`
- **Scheme files** (`.scm`): + `opencog-scheme.instructions.md`
- **Shell scripts** (`.sh`): + `shell.instructions.md`
- **CI/CD** (`.github/workflows/`): + `github-actions-ci-cd-best-practices.instructions.md`

## Memory Bank

Cross-session context persists in `memory-bank/`:
- `projectbrief.md` — What this project is
- `productContext.md` — How it works and why
- `techContext.md` — Technical stack and constraints
- `activeContext.md` — Current sprint state (update each session)
- `systemPatterns.md` — Architecture and code patterns

## Sprint Templates

Find templates in `docs/templates/`:
- `sprint-plan-template.md` — Sprint planning
- `sprint-done-template.md` — Sprint completion
- `qa-signoff-template.md` — QA sign-off