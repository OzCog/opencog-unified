# AI Team Orchestration Guide — OpenCog Unified

## Overview

This project uses a multi-agent AI team workflow where different AI personas handle different aspects of development. The human (you) acts as the message bus between parallel chats.

## Quick Start

### 1. Set Up Parallel Clones

```bash
# Dev team clone
git clone https://github.com/OzCog/opencog-unified.git opencog-dev
cd opencog-dev && git checkout -b feature/sprint-1

# QA clone (after dev merges)
git clone https://github.com/OzCog/opencog-unified.git opencog-qa
cd opencog-qa && git checkout -b feature/qa-1

# DevOps clone (on demand)
git clone https://github.com/OzCog/opencog-unified.git opencog-devops
cd opencog-devops && git checkout -b feature/devops-1
```

### 2. Start a Sprint

1. Open Producer chat → give cold start prompt from `docs/team/chat-prompts.md`
2. Producer drafts `docs/sprint-N/plan.md`
3. Run team consilium (optional but recommended for major sprints)
4. Open Dev Team chat → give cold start prompt + sprint plan
5. Dev team executes, pushes PR
6. Open QA chat → give sign-off prompt
7. QA validates, files issues or signs off
8. Producer merges PR

### 3. Sprint Lifecycle

```
Planning → Consilium → Execution → PR → QA → Fix → Merge → Handoff
   Remy      All         Dev       Dev   Ivy   Dev   Remy    All
```

## Key Principles

### Context Is King
- `PROJECT_BRIEF.md` is the single source of truth
- `docs/sprint-N/progress.md` enables context recovery
- `docs/sprint-N/done.md` is mandatory at sprint end
- The repo is shared memory — keep it accurate

### Build Times Matter
This is NOT a web app with instant feedback loops:
- Full build: 30-60 minutes
- Phase integration: 5-10 minutes each
- Validation: 2-5 minutes
- Plan work in phases, not rapid iterations

### Dependency Order Is Critical
```
cogutil → atomspace → (rocks, restful) → unify → ure → (attention, spacetime) → pln → (miner, moses, asmoses) → (lg-atomese, learn) → opencog
```
Breaking dependency order = broken builds. Always validate.

## Sprint Cadence

### For OpenCog Unified
Given 30-60 min build times and complex integration:
- **Sprint duration:** 1-2 weeks (not days)
- **Scope per sprint:** 1 integration phase (3-4 components max)
- **Build budget:** 2-3 full builds per sprint (validate start, mid, end)
- **QA window:** Full day minimum (validation + phase tests)

### Suggested Sprint Sequence

| Sprint | Focus | Components |
|--------|-------|------------|
| 1 | Phase 1 Stabilization | atomspace-rocks, atomspace-restful, moses |
| 2 | Phase 2 Logic Systems | unify, ure, language-learning |
| 3 | Phase 3 Cognitive | attention, spacetime |
| 4 | Phase 4 Advanced | pln, miner, asmoses |
| 5 | Phase 5 Integration | lg-atomese, learn, opencog |
| 6 | Polish & Testing | Full system validation, docs |

## Anti-Patterns (Critical for This Project)

| Don't | Do Instead | Why |
|-------|------------|-----|
| Cancel long builds | Wait 60+ min | Builds WILL complete — canceling wastes all progress |
| Skip dependency order | Always build bottom-up | Upper components fail without lower ones |
| Batch all fixes | One commit per fix per component | Makes reverts possible |
| Test all phases at once | Validate phase-by-phase | Isolate failures to specific components |
| Skip progress.md updates | Update after each phase | 60-min builds = high recovery cost |

## Files Reference

| File | Purpose | Updated By |
|------|---------|------------|
| `PROJECT_BRIEF.md` | Single source of truth | All teams (sections 7-8 each sprint) |
| `docs/sprint-N/plan.md` | Sprint tasks and criteria | Remy (Producer) |
| `docs/sprint-N/progress.md` | Live progress tracker | Dev Team (during sprint) |
| `docs/sprint-N/done.md` | Sprint handoff document | Dev Team (sprint end) |
| `docs/qa/sprint-N-signoff.md` | QA validation report | Ivy (QA) |
| `docs/team/chat-prompts.md` | Team role prompts | Remy (as needed) |
| `docs/brainstorm/*.md` | Design session outputs | Full team |

## Workflows

### Standard Development Workflow
```
1. Remy drafts sprint plan
2. Dev team pulls main, creates feature/sprint-N
3. Dev builds phase-by-phase (30-60 min each build)
4. Dev updates progress.md after each phase
5. Dev pushes PR when all success criteria met
6. Ivy runs validation on merged main
7. Ivy files issues or signs off
8. Remy merges PR, updates PROJECT_BRIEF.md
```

### Context Recovery Workflow
```
1. Save: Update progress.md + PROJECT_BRIEF.md sections 7-8
2. Close old chat
3. Open new chat with recovery prompt:
   "Read PROJECT_BRIEF.md and docs/sprint-N/progress.md.
    Continue from where it left off."
```

### Emergency Fix Workflow
```
1. Ivy files blocker issue on GitHub
2. Remy triages, assigns to dev team
3. Dev fixes on feature/sprint-N (single commit, refs issue)
4. Ivy verifies fix
5. Remy merges
```

### Brainstorm Workflow (Major Decisions)
```
1. Open brainstorm chat with full team prompt
2. Run 3 phases: ideation → debate → pitches
3. Save outputs to docs/brainstorm/
4. Human (CEO) makes final decision
5. Decision feeds into next sprint plan
```
