# Sprint N — [Name]

> Sprint Goal: [one sentence describing the deliverable]
> Branch: feature/sprint-N
> Estimated effort: [time estimate]
> Phase focus: [1-5]

## Prioritized Task List

| # | Task | Owner | Est | Phase | Description |
|---|------|-------|-----|-------|-------------|
| 1 | [task] | Nova | 2h | Core | [C++ implementation details] |
| 2 | [task] | Sage | 1h | Logic | [Scheme rule/binding work] |
| 3 | [task] | Milo | 1h | Research | [Algorithm design] |
| 4 | [task] | Kira | 30m | Arch | [Design review/decisions] |

## Work Schedule

### Phase 1: Foundation (tasks 1-2)
- Build [component]
- Validate: `./validate-integration.py --phase [N]`
- Checkpoint commit after phase

### Phase 2: Integration (tasks 3-4)
- Build [component]
- Run tests: `cd tests/integration && python3 -m pytest -v`
- Checkpoint commit after phase

## Dependencies & Risks
- [Risk 1]: Mitigation strategy
- [Risk 2]: Fallback plan

## Build Notes
- Full rebuild expected: ~45 min
- Phase-only rebuild: ~10 min
- NEVER cancel long-running builds

## Success Criteria
- [ ] Build completes without new errors
- [ ] Phase validation passes
- [ ] Integration tests pass
- [ ] No new placeholder code
- [ ] QA sign-off obtained
