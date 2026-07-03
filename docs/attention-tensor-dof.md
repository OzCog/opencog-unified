# Attention Tensor Degrees of Freedom

This document describes the degrees of freedom (DOF) in the OpenCog ECAN (Economic Attention Networks) attention system, covering the full parameter space that governs attention allocation dynamics.

## Overview

The ECAN attention system models attention as an economic resource distributed across atoms in the AtomSpace. The "attention tensor" refers to the multi-dimensional parameter space that controls how attention flows, decays, and self-organizes across the cognitive system.

## Primary Attention Dimensions

### 1. Short-Term Importance (STI)

| Parameter | Range | Description |
|-----------|-------|-------------|
| `sti_value` | [-∞, +∞] | Current short-term importance of an atom |
| `attentional_focus_boundary` | [0, +∞] | Threshold for entering the attentional focus set |
| `sti_decay_rate` | [0, 1] | Rate at which STI decays per cycle (default: 0.05) |

STI determines which atoms are "in focus" at any given moment. Atoms above the attentional focus boundary are actively considered for cognitive processing.

### 2. Long-Term Importance (LTI)

| Parameter | Range | Description |
|-----------|-------|-------------|
| `lti_value` | [0, +∞] | Long-term importance (persistence) of an atom |
| `lti_refresh_threshold` | [0, +∞] | Minimum LTI below which atoms risk forgetting |
| `lti_decay_rate` | [0, 1] | Rate of LTI decay per cycle (default: 0.01) |

LTI determines which atoms persist in memory. Atoms with low LTI may be removed by the ForgettingAgent.

## Economic Parameters (Attention Currency)

### 3. Rent/Wages/Tax Rates

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `rent_rate` | [0, 1] | 0.01 | STI cost per cycle for atoms in attentional focus |
| `wage_rate` | [0, 1] | 0.05 | STI reward for atoms that contribute to useful inferences |
| `tax_rate` | [0, 1] | 0.02 | Redistribution rate from high-STI to low-STI atoms |
| `total_sti_budget` | [0, +∞] | 1000.0 | Total STI available in the system (conserved quantity) |

The economic model ensures attention is a finite, conserved resource. Productive atoms earn wages; unproductive atoms pay rent and decay.

### 4. Spreading Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `spreading_rate` | [0, 1] | 0.3 | Fraction of STI spread to neighbors per cycle |
| `max_spread_distance` | [1, +∞] | 3 | Maximum hops for recursive attention spreading |
| `hebbian_link_weight` | [0, 1] | — | Connection strength between atoms (per-link) |
| `spreading_threshold` | [0, +∞] | 10.0 | Minimum STI required to be a spreading source |
| `inverse_distance_decay` | [0, 1] | 0.5 | How much spreading diminishes per hop |

Spreading follows HebbianLinks with importance proportional to link weight and inversely proportional to graph distance.

## Cross-Agent Synchronization Parameters

### 5. Multi-Agent Dynamics

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `sync_interval_ms` | [0, +∞] | 100.0 | How often agents synchronize states |
| `sync_strategy` | enum | BATCHED | IMMEDIATE, BATCHED, LAZY, PERIODIC |
| `conflict_resolution` | enum | LAST_WRITER_WINS | Conflict resolution policy |
| `merge_weight_local` | [0, 1] | 0.7 | Weight for local state in merge operations |
| `merge_weight_remote` | [0, 1] | 0.3 | Weight for remote state in merge operations |

### 6. Resource Allocation Strategies

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `allocation_strategy` | enum | ADAPTIVE_HYBRID | Resource allocation policy |
| `fairness_weight` | [0, 1] | 0.3 | Weight of fairness vs. performance in allocation |
| `demand_elasticity` | [0, +∞] | 1.5 | How responsive allocation is to demand changes |
| `gini_target` | [0, 1] | 0.4 | Target Gini coefficient for inequality bounds |

## Emergent Dynamics DOF

### 7. Oscillation-Related Parameters

| Parameter | Range | Description |
|-----------|-------|-------------|
| `cycle_frequency` | [0.1, 1000] Hz | Processing loop speed per agent |
| `coupling_strength` | [0, 1] | How strongly agents influence each other |
| `phase_noise` | [0, +∞] | Stochastic noise in agent phase relationships |
| `resonance_bandwidth` | [0, +∞] | Frequency range for synchronization lock-in |

Emergent oscillations arise from the interplay of attention spreading, economic feedback, and multi-agent coupling. The system can exhibit:

- **Attention waves**: Periodic sweeps of high-STI across the AtomSpace graph
- **Focus oscillations**: Alternating expansion/contraction of the attentional focus
- **Phase-locked agent clusters**: Groups of agents that synchronize their cognitive cycles
- **Chaotic attractors**: Non-periodic but bounded attention dynamics under certain parameter regimes

### 8. Temporal-Spatial Parameters (SpaceTime Module)

| Parameter | Range | Description |
|-----------|-------|-------------|
| `spatial_decay` | [0, 1] | Distance-based attention decay in spatial reasoning |
| `temporal_window` | [0, +∞] s | Time horizon for temporal attention allocation |
| `spatial_resolution` | [0, +∞] | Granularity of spatial attention map |

## Tensor Representation

The full attention state can be represented as a tensor:

```
A[agent_i, atom_j, time_t] = {STI, LTI, spread_rate, economic_state}
```

**Dimensions:**
- Agent index `i ∈ [0, N_agents)` — which cognitive agent
- Atom index `j ∈ [0, N_atoms)` — which atom in the AtomSpace
- Time index `t ∈ [0, T)` — discrete time step
- Value: tuple of (STI, LTI, local_spread_rate, economic_balance)

**Total DOF count:**

| Category | Degrees of Freedom |
|----------|-------------------|
| Per-atom STI/LTI | 2 × N_atoms |
| Economic rates (global) | 4 (rent, wage, tax, budget) |
| Spreading parameters (global) | 5 |
| Per-link weights | N_links |
| Sync parameters | 5 |
| Per-agent parameters | 4 × N_agents |
| Temporal-spatial | 3 |
| **Total** | **2N + E + 4A + 17** |

Where N = number of atoms, E = number of links, A = number of agents.

## Phase Space Exploration

The system's behavior depends critically on the ratios between parameters:

1. **Rent/Wage ratio** > 1: Attention concentrates (winner-take-all)
2. **Rent/Wage ratio** < 1: Attention disperses (democratic)
3. **Spreading rate × max distance** > 1: Cascading activation
4. **Spreading rate × max distance** < 1: Local attention pools
5. **Sync interval / cycle frequency** ≪ 1: Tight coupling (synchronized)
6. **Sync interval / cycle frequency** ≫ 1: Loose coupling (independent)

## References

- OpenCog ECAN specification: `attention/opencog/attention/ECANAgent.h`
- Distributed sync: `distributed-cognition/include/DistributedAtomSpaceSync.h`
- Resource allocation: `distributed-cognition/include/ECANResourceManager.h`
- Tensor protocol: `distributed-cognition/include/TensorHypergraphProtocol.h`
