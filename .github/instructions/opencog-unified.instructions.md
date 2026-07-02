---
description: 'OpenCog Unified project-wide instructions for GitHub Copilot. Activates automatically for all files in this repository.'
applyTo: '**'
---

# OpenCog Unified — Copilot Context

This is a **cognitive architecture monorepo** implementing the OpenCog AGI framework in C++ with Guile/Scheme bindings.

## Project Identity
- **14+ integrated components** for artificial general intelligence
- **Hypergraph knowledge store** (AtomSpace) as the central data structure
- **CMake build system** with complex inter-component dependencies
- **Build time: 30-60 minutes** — never cancel long-running builds

## Component Dependency Order (CRITICAL)
```
cogutil → atomspace → cogserver → {atomspace-rocks, atomspace-restful}
atomspace → unify → ure → {pln, miner, asmoses}
atomspace → {attention, spacetime, lg-atomese, learn}
cogutil → {moses, language-learning}
all → opencog (integration)
```

## Team Personas (use @agent-name to invoke)
- **@nova-cpp** — C++ core, AtomSpace, CMake, build system
- **@sage-scheme** — Guile/Scheme, URE rules, PLN, pattern matching
- **@milo-research** — Algorithms, MOSES, attention dynamics, papers
- **@kira-architect** — System design, component interactions, AGI patterns
- **@ivy-qa** — Testing, validation, bug filing (never fixes code)
- **@remy-producer** — Sprint planning, coordination (never writes code)
- **@dash-devops** — CI/CD, Docker, build infrastructure

## Key Conventions
- C++ files: OpenCog naming (CamelCase classes, snake_case functions)
- Scheme files: Kebab-case, `define-public` for exports
- Commits: `fix:`, `feat:`, `refactor:` prefixes + `Fixes #N` for issues
- Tests: `tests/integration/test_*.py` pattern
- Validation: `./validate-integration.py --phase [1-5]`
