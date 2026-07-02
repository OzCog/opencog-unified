# Technical Context — OpenCog Unified

## Build System
- CMake 3.16+ required
- Pattern: `add_subdirectory(component)` if exists
- Parallel builds: `make -j$(nproc)` (NEVER cancel)
- Clean builds: `rm -rf build && mkdir build && cd build && cmake ..`

## Dependencies
| Package | Purpose | Required |
|---------|---------|----------|
| libboost-all-dev | Core utilities, threading | Yes |
| guile-2.2-dev / guile-3.0-dev | Scheme bindings | Yes |
| librocksdb-dev | Persistent storage | Yes |
| python3-dev | Python bindings | Yes |
| cmake | Build system | Yes |
| build-essential | Compiler toolchain | Yes |

## Component Build Order
1. cogutil (foundation, no deps)
2. atomspace (depends on cogutil)
3. cogserver (depends on atomspace)
4. atomspace-rocks, atomspace-restful (depend on atomspace)
5. unify (depends on atomspace)
6. ure (depends on unify)
7. attention (depends on atomspace, cogserver)
8. spacetime (depends on atomspace)
9. pln (depends on ure, spacetime)
10. miner (depends on ure)
11. asmoses (depends on ure)
12. moses (depends on cogutil)
13. lg-atomese, learn (depend on atomspace)
14. opencog (depends on everything)

## Validation Commands
```bash
./validate-integration.py           # Full validation
./validate-integration.py --phase N # Phase-specific
cd tests/integration && python3 -m pytest -v  # Integration tests
```

## Known Constraints
- Windows not supported (Linux/macOS only)
- Guile 2.2 vs 3.0 compatibility issues on newer Ubuntu
- RocksDB version mismatches can cause link errors
- Full rebuild required after CMake changes
