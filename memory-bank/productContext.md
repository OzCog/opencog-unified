# Product Context — OpenCog Unified

## Why This Exists
Individual OpenCog components were scattered across 20+ repositories with incompatible versions, broken cross-references, and no unified build. This monorepo solves the integration problem.

## How It Works
1. All components live in top-level directories
2. A single CMakeLists.txt orchestrates the build
3. `integrate-components.sh` pulls from upstream repos
4. `validate-integration.py` verifies all components work together
5. Phase-based testing validates each subsystem independently

## Cognitive Architecture Layers
- **Foundation**: cogutil (logging, types, threading)
- **Knowledge**: AtomSpace (hypergraph, truth values, attention values)
- **Infrastructure**: CogServer (distributed), RocksDB (persistence), REST API
- **Reasoning**: URE (rule engine) → PLN (probabilistic logic)
- **Learning**: MOSES (evolutionary), Pattern Miner (data mining)
- **Perception**: Attention (ECAN), Spacetime (spatial reasoning)
- **Language**: Link Grammar, Unsupervised Learning
- **Integration**: OpenCog meta-component

## User Interaction
- Build and test via command line
- Interact via CogServer (network protocol)
- Query via REST API or Scheme REPL
- Persist via RocksDB backend
