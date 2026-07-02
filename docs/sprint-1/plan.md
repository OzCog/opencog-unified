# Sprint 1 — Phase 1 Stabilization

> Sprint Goal: Validate and stabilize Phase 1 components (atomspace-rocks, atomspace-restful, moses)
> Branch: feature/sprint-1
> Estimated effort: 1-2 weeks

## Prioritized Task List

| # | Task | Owner | Est | Description |
|---|------|-------|-----|-------------|
| 1 | Validate atomspace-rocks build | Nova | 2h | Ensure RocksDB backend compiles and links correctly |
| 2 | Validate atomspace-restful build | Nova | 2h | Ensure REST API component compiles |
| 3 | Validate moses build | Nova/Milo | 2h | Ensure MOSES evolutionary optimizer builds |
| 4 | Integration test: atomspace-rocks | Sage | 1h | Run test_atomspace-rocks.py, fix failures |
| 5 | Integration test: atomspace-restful | Sage | 1h | Run test_atomspace-restful.py, fix failures |
| 6 | Integration test: moses | Milo | 1h | Run test_moses.py, fix failures |
| 7 | Phase 1 validation | Ivy | 1h | Run ./validate-integration.py --phase 1 |
| 8 | CMake dependency audit | Nova | 1h | Verify Phase 1 deps in CMakeLists.txt |

## Work Schedule

### Phase 1: Build Validation (tasks 1-3)
- Clean rebuild with Phase 1 components
- Fix compilation errors
- Checkpoint commit after all three build

### Phase 2: Integration Testing (tasks 4-6)
- Run individual component tests
- Fix any runtime failures
- Checkpoint commit

### Phase 3: Validation & Audit (tasks 7-8)
- Full phase validation
- CMake dependency graph verification
- Final commit + PR

## Success Criteria

- [ ] `cmake .. && make -j$(nproc)` completes without errors for Phase 1 components
- [ ] `python3 test_atomspace-rocks.py` passes
- [ ] `python3 test_atomspace-restful.py` passes
- [ ] `python3 test_moses.py` passes
- [ ] `./validate-integration.py --phase 1` reports SUCCESS
- [ ] No new compilation warnings introduced
- [ ] All commits reference relevant GitHub Issues

## What's NOT in This Sprint

| Feature | Reason |
|---------|--------|
| Phase 2-5 components | Sequential dependency — Phase 1 must pass first |
| Performance optimization | Correctness first |
| New features/algorithms | Stabilization sprint, not development |
| CI/CD pipeline | Separate DevOps sprint |

## Agent Prompt

> Read PROJECT_BRIEF.md, then read docs/sprint-1/plan.md. Execute Sprint 1.
>
> First: git pull origin main && git checkout -b feature/sprint-1
>
> CRITICAL: Build takes 30-60 minutes. NEVER CANCEL. Set timeout to 90+ minutes.
> Follow dependency order: cogutil → atomspace → Phase 1 components.
>
> Close GitHub Issues in commits: "fix: description (Fixes #NN)"
> Update docs/sprint-1/progress.md after each phase.
> When done, push and create PR: git push origin feature/sprint-1
> Follow Sections 12-14 of PROJECT_BRIEF.md.
