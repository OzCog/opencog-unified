# System Patterns — OpenCog Unified

## Architecture Pattern: Hypergraph-Centric
Everything is an Atom. All components communicate via the AtomSpace.
No direct coupling between cognitive subsystems.

## Build Pattern: Phase-Based Integration
```
Phase 1: Core Extensions (atomspace-rocks, atomspace-restful)
Phase 2: Logic Systems (unify, ure)
Phase 3: Cognitive Systems (attention, spacetime)
Phase 4: Advanced & Learning (pln, miner, asmoses, moses)
Phase 5: Language & Integration (lg-atomese, learn, opencog)
```

## Code Pattern: Atom Factory
```cpp
// Never construct Atoms directly — use AtomSpace factory
Handle h = as->add_node(CONCEPT_NODE, "name");
Handle l = as->add_link(INHERITANCE_LINK, HandleSeq{h1, h2});
```

## Code Pattern: Scheme Rule Definition
```scheme
(DefineLink
  (DefinedSchemaNode "rule-name")
  (BindLink (VariableList ...) (AndLink ...) (ExecutionOutputLink ...)))
```

## Testing Pattern: Validate Per Phase
```bash
./validate-integration.py --phase N  # Quick feedback
./validate-integration.py            # Full validation before PR
```

## Git Pattern: Sprint Branches
```
main ← feature/sprint-N (dev work)
     ← feature/qa-N (QA testing)
     ← feature/devops-N (infra work)
```

## Documentation Pattern: Sprint Lifecycle
```
docs/sprint-N/plan.md      → Before sprint
docs/sprint-N/progress.md  → During sprint
docs/sprint-N/done.md      → After sprint
docs/qa/sprint-N-signoff.md → QA sign-off
```
