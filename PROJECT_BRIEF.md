# PROJECT_BRIEF.md — OpenCog Unified

> Last updated: 2026-07-02 | Sprint 0 | Status: Architecture & Orchestration Setup

## 1. Project Overview

OpenCog Unified is a comprehensive cognitive architecture monorepo integrating 14+ OpenCog components into a unified framework for artificial general intelligence (AGI) development. The system implements neural-symbolic reasoning, distributed cognition, evolutionary optimization, probabilistic logic, and natural language processing. Target users are AGI researchers, cognitive scientists, and developers building intelligent systems.

## 2. Concept / Product Description

A unified AGI framework providing:
- **Hypergraph knowledge representation** (AtomSpace) — flexible, typed knowledge graphs
- **Probabilistic reasoning** (PLN) — uncertain inference with truth values
- **Evolutionary program synthesis** (MOSES) — automated program generation
- **Economic attention allocation** (ECAN) — dynamic resource management
- **Neural-symbolic integration** — bridging connectionist and symbolic AI
- **Distributed cognitive processing** — multi-agent cognition coordination
- **Natural language processing** — unsupervised grammar learning

Key user flows:
1. Researcher defines knowledge in AtomSpace → applies PLN inference → mines patterns
2. Developer deploys CogServer → connects distributed agents → runs cognitive workloads
3. Language scientist trains grammar learner → integrates with Link Grammar → generates atomese

## 3. Tech Stack

- **Languages:** C++ (core), Scheme/Guile (scripting/DSL), Python (bindings/tests)
- **Build:** CMake (unified build system)
- **Storage:** RocksDB (persistent AtomSpace), REST API (external access)
- **Testing:** Python pytest, CTest, custom integration suites
- **CI/CD:** GitHub Actions
- **Dependencies:** Boost, Guile 2.2/3.0, RocksDB, Link Grammar
- **Platform:** Linux (Ubuntu/Debian primary)

## 4. Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Integration Layer (opencog)                       │
├─────────────────────────────────────────────────────────────────────┤
│  Language Processing       │  Learning & Optimization               │
│  ├── lg-atomese            │  ├── moses                             │
│  ├── learn                 │  ├── asmoses                           │
│  └── language-learning     │  └── miner                             │
├────────────────────────────┼────────────────────────────────────────┤
│  Cognitive Systems         │  Advanced Logic                        │
│  ├── attention (ECAN)      │  ├── pln                               │
│  └── spacetime             │  └── (depends on ure + spacetime)      │
├────────────────────────────┼────────────────────────────────────────┤
│  Logic & Reasoning         │  Storage Backends                      │
│  ├── unify                 │  ├── atomspace-rocks (RocksDB)         │
│  └── ure                   │  └── atomspace-restful (REST API)      │
├─────────────────────────────────────────────────────────────────────┤
│              Core Layer: atomspace + cogserver                       │
├─────────────────────────────────────────────────────────────────────┤
│              Foundation: cogutil                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 5. Key Files Map

| Area | Path | Contents |
|------|------|----------|
| Build system | `CMakeLists.txt` | Root CMake configuration |
| Component config | `component-config.json` | Dependencies & phase assignments |
| Integration script | `integrate-components.sh` | Component cloning/setup |
| Validation | `validate-integration.py` | Multi-phase validation |
| Tests | `tests/integration/` | Component integration tests |
| Sprint docs | `docs/sprint-N/` | Plans, progress, done |
| Team docs | `docs/team/` | Team orchestration references |
| Foundation | `cogutil/` | Core utilities (build first) |
| Knowledge | `atomspace/` | Hypergraph knowledge engine |
| Server | `cogserver/` | Distributed cognitive server |
| Storage | `atomspace-rocks/` | RocksDB persistence |
| Logic | `unify/`, `ure/` | Pattern matching & rule engine |
| Reasoning | `pln/` | Probabilistic logic networks |
| Attention | `attention/` | ECAN attention allocation |
| Learning | `moses/`, `asmoses/` | Evolutionary optimization |
| Language | `lg-atomese/`, `learn/` | NLP pipeline |
| Integration | `opencog/` | Final unified component |

## 6. Team Roles

| Agent | Name | Role | Focus |
|-------|------|------|-------|
| Producer | **Remy** | Sprint planning, coordination, merging | Scope control, phase ordering, dependency tracking |
| Cognitive Architect | **Kira** | System design, component interactions | AGI patterns, cognitive architecture decisions |
| Core Engineer | **Nova** | C++ implementation, AtomSpace, build system | Component integration, CMake, performance |
| Logic/Scheme Engineer | **Sage** | Scheme bindings, rule engines, PLN | Guile/Scheme, URE rules, inference chains |
| Systems Engineer | **Dash** | CI/CD, build infrastructure, deployment | GitHub Actions, Docker, dependency management |
| QA Engineer | **Ivy** | Integration testing, validation, phase sign-off | pytest, validate-integration.py, component tests |
| Research Lead | **Milo** | Algorithm design, paper implementations | MOSES, PLN theory, attention dynamics |

## 7. Sprint Status

| Sprint | Name | Status | Scope |
|--------|------|--------|-------|
| 0 | Architecture & Orchestration | 🔨 In Progress | Team setup, PROJECT_BRIEF, sprint structure |
| 1 | Phase 1 Stabilization | ⬜ Planned | atomspace-rocks, atomspace-restful, moses validation |

## 8. Current State (rewrite every sprint)

**What works:**
- Foundation layer (cogutil) is present and builds
- Core layer (atomspace, cogserver) is present
- All 14+ components are integrated in repository
- 5-phase integration pipeline defined
- Validation framework operational
- Integration tests for core components

**What doesn't work yet:**
- Full multi-threaded build not verified on all phases
- Some components have placeholder implementations (700+ TODOs expected)
- Cross-component integration testing incomplete
- CI/CD pipeline needs enhancement

**What's next:**
- Complete Sprint 0 orchestration setup
- Stabilize Phase 1 components (atomspace-rocks, atomspace-restful, moses)
- Run full validation pipeline
- Begin Sprint 1 execution

## 9. Security Rules

1. Secrets live in environment variables only — never in code or git
2. No API keys or credentials in source files
3. CogServer network access configured via environment
4. RocksDB paths configured externally
5. REST API authentication required for production deployments

## 10. How to Run Locally

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y cmake build-essential libboost-all-dev \
    python3-dev guile-2.2-dev librocksdb-dev

# Build
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)  # Takes 30-60 minutes — NEVER CANCEL

# Validate
cd ..
./validate-integration.py

# Run tests
cd tests/integration
python3 -m pytest -v
```

## 11. How to Deploy

```bash
# Docker (recommended for deployment)
docker build -t opencog-unified .
docker run -p 17001:17001 opencog-unified

# Manual deployment
cd build && make install
# CogServer starts on port 17001 by default
cogserver --config /etc/opencog/cogserver.conf
```

## 12. Cross-Chat Handoff Protocol

Every sprint chat must do these before finishing:

1. Write `docs/sprint-N/done.md` — what was built, components touched, what's not done
2. Update PROJECT_BRIEF.md: Section 7 (mark sprint done) + Section 8 (rewrite current state)
3. Commit all changes with descriptive message: `sprint-N: <summary>`
4. Update `docs/sprint-N/progress.md` with final status

**Context recovery prompt:**
```
Read PROJECT_BRIEF.md, then read docs/sprint-N/progress.md.
Continue from where it left off.
```

This is how context survives across chats. The repo is shared memory — keep it accurate.

## 13. Bug & Fix Tracking

Bugs are tracked as GitHub Issues on OzCog/opencog-unified.

**For QA:** File bugs as GitHub Issues with labels (`bug`, `phase-N`, `component:name`). Include: component, build/test output, expected vs actual.

**For Dev Team:** Check GitHub Issues before starting work. Fix blockers first. Use closing keywords: `fix: description (Fixes #NN)`.

**For Build Issues:** Label with `build`, include CMake/make output and platform info.

**For feature ideas:** Add to `docs/ideas-backlog.md`.

## 14. Multi-Repo Setup

Each team works in their own separate clone:

**Teams:**
- Producer on `main` (coordination hub)
- Dev Team on `feature/sprint-N`
- QA on `feature/qa-N`
- DevOps on `feature/devops-N` (only when needed)

**Setup:**
```bash
git clone https://github.com/OzCog/opencog-unified.git opencog-dev
cd opencog-dev
git checkout -b feature/sprint-N
# Install dependencies and build
```

**Branch strategy:** Feature branches → PR → regular merge to main. Never push directly to main. Never squash. Never rebase feature branches.

**Build before merge:** All PRs must pass `./validate-integration.py` before merge.
