#!/usr/bin/env python3
"""
ECAN Attention Simulation Test
Issue #218: Cognitive Layer — Distributed Cognition Dynamics

Simulates multiple cycles of ECAN attention allocation across a synthetic
atom network. Validates rent collection, wage payment, tax redistribution,
attention spreading, decay, and convergence properties.

Outputs JSON metrics for analysis.
"""

import json
import math
import random
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple


@dataclass
class Atom:
    """Represents an atom in the AtomSpace with attention values."""
    atom_id: str
    sti: float = 0.0          # Short-Term Importance
    lti: float = 0.0          # Long-Term Importance
    neighbors: List[str] = field(default_factory=list)
    link_weights: Dict[str, float] = field(default_factory=dict)
    useful: bool = False      # Whether atom contributed to inference


@dataclass
class ECANConfig:
    """Configuration parameters for ECAN simulation."""
    rent_rate: float = 0.01
    wage_rate: float = 0.05
    tax_rate: float = 0.02
    spreading_rate: float = 0.3
    max_spread_distance: int = 3
    sti_decay_rate: float = 0.05
    lti_decay_rate: float = 0.01
    total_sti_budget: float = 1000.0
    attentional_focus_boundary: float = 50.0
    spreading_threshold: float = 10.0


@dataclass
class CycleMetrics:
    """Metrics for a single ECAN cycle."""
    cycle: int
    total_sti: float
    mean_sti: float
    max_sti: float
    min_sti: float
    std_sti: float
    atoms_in_focus: int
    rent_collected: float
    wages_paid: float
    tax_redistributed: float
    attention_spread: float
    gini_coefficient: float


class ECANSimulator:
    """Simulates ECAN attention allocation dynamics."""

    def __init__(self, config: ECANConfig, num_atoms: int = 100, seed: int = 42):
        self.config = config
        self.rng = random.Random(seed)
        self.atoms: Dict[str, Atom] = {}
        self.cycle_history: List[CycleMetrics] = []
        self._build_network(num_atoms)

    def _build_network(self, num_atoms: int):
        """Build a scale-free-like network of atoms."""
        for i in range(num_atoms):
            atom_id = f"atom_{i:04d}"
            self.atoms[atom_id] = Atom(
                atom_id=atom_id,
                sti=self.rng.gauss(50.0, 20.0),
                lti=self.rng.uniform(10.0, 50.0),
                useful=(self.rng.random() < 0.2)
            )

        # Create edges (preferential attachment)
        atom_ids = list(self.atoms.keys())
        for i, atom_id in enumerate(atom_ids):
            num_links = min(self.rng.randint(2, 6), len(atom_ids) - 1)
            targets = self.rng.sample(
                [a for a in atom_ids if a != atom_id],
                k=num_links
            )
            for target in targets:
                weight = self.rng.uniform(0.1, 1.0)
                self.atoms[atom_id].neighbors.append(target)
                self.atoms[atom_id].link_weights[target] = weight
                # Bidirectional
                if atom_id not in self.atoms[target].neighbors:
                    self.atoms[target].neighbors.append(atom_id)
                    self.atoms[target].link_weights[atom_id] = weight

    def run_cycle(self, cycle_num: int) -> CycleMetrics:
        """Execute one complete ECAN cycle."""
        rent_collected = self._collect_rent()
        wages_paid = self._pay_wages()
        tax_redistributed = self._collect_tax()
        attention_spread = self._spread_attention()
        self._apply_decay()
        self._normalize_budget()

        metrics = self._compute_metrics(cycle_num)
        metrics.rent_collected = rent_collected
        metrics.wages_paid = wages_paid
        metrics.tax_redistributed = tax_redistributed
        metrics.attention_spread = attention_spread
        self.cycle_history.append(metrics)
        return metrics

    def _collect_rent(self) -> float:
        """Collect rent from atoms in attentional focus."""
        total_rent = 0.0
        for atom in self.atoms.values():
            if atom.sti > self.config.attentional_focus_boundary:
                rent = atom.sti * self.config.rent_rate
                atom.sti -= rent
                total_rent += rent
        return total_rent

    def _pay_wages(self) -> float:
        """Pay wages to atoms that contribute to useful inferences."""
        total_wages = 0.0
        for atom in self.atoms.values():
            if atom.useful:
                wage = self.config.wage_rate * self.config.total_sti_budget / max(
                    1, sum(1 for a in self.atoms.values() if a.useful))
                atom.sti += wage
                total_wages += wage
                # Randomly toggle usefulness for dynamics
                if self.rng.random() < 0.1:
                    atom.useful = False
            elif self.rng.random() < 0.05:
                atom.useful = True
        return total_wages

    def _collect_tax(self) -> float:
        """Redistribute attention from rich to poor atoms."""
        total_tax = 0.0
        sti_values = [a.sti for a in self.atoms.values()]
        mean_sti = sum(sti_values) / len(sti_values)

        for atom in self.atoms.values():
            if atom.sti > mean_sti * 2:
                tax = (atom.sti - mean_sti) * self.config.tax_rate
                atom.sti -= tax
                total_tax += tax

        # Redistribute to low-STI atoms
        low_sti_atoms = [a for a in self.atoms.values()
                         if a.sti < mean_sti * 0.5]
        if low_sti_atoms and total_tax > 0:
            share = total_tax / len(low_sti_atoms)
            for atom in low_sti_atoms:
                atom.sti += share

        return total_tax

    def _spread_attention(self) -> float:
        """Spread attention along HebbianLinks."""
        total_spread = 0.0
        spread_updates: Dict[str, float] = {}

        for atom in self.atoms.values():
            if atom.sti < self.config.spreading_threshold:
                continue

            spread_amount = atom.sti * self.config.spreading_rate
            total_weight = sum(atom.link_weights.values())
            if total_weight == 0:
                continue

            for neighbor_id, weight in atom.link_weights.items():
                share = spread_amount * (weight / total_weight)
                spread_updates[neighbor_id] = spread_updates.get(
                    neighbor_id, 0.0) + share
                total_spread += share

            atom.sti -= spread_amount

        # Apply spread updates
        for atom_id, delta in spread_updates.items():
            if atom_id in self.atoms:
                self.atoms[atom_id].sti += delta

        return total_spread

    def _apply_decay(self):
        """Apply temporal decay to STI and LTI."""
        for atom in self.atoms.values():
            atom.sti *= (1.0 - self.config.sti_decay_rate)
            atom.lti *= (1.0 - self.config.lti_decay_rate)

    def _normalize_budget(self):
        """Ensure total STI stays near budget (soft normalization)."""
        total_sti = sum(a.sti for a in self.atoms.values())
        if total_sti > 0:
            scale = self.config.total_sti_budget / total_sti
            # Soft normalization (blend toward budget)
            blend = 0.1
            effective_scale = 1.0 + blend * (scale - 1.0)
            for atom in self.atoms.values():
                atom.sti *= effective_scale

    def _compute_metrics(self, cycle_num: int) -> CycleMetrics:
        """Compute aggregate metrics for the current cycle."""
        sti_values = [a.sti for a in self.atoms.values()]
        n = len(sti_values)
        mean_sti = sum(sti_values) / n
        max_sti = max(sti_values)
        min_sti = min(sti_values)
        variance = sum((s - mean_sti) ** 2 for s in sti_values) / n
        std_sti = math.sqrt(variance)
        atoms_in_focus = sum(
            1 for s in sti_values if s > self.config.attentional_focus_boundary)
        gini = self._gini_coefficient(sti_values)

        return CycleMetrics(
            cycle=cycle_num,
            total_sti=sum(sti_values),
            mean_sti=mean_sti,
            max_sti=max_sti,
            min_sti=min_sti,
            std_sti=std_sti,
            atoms_in_focus=atoms_in_focus,
            rent_collected=0.0,
            wages_paid=0.0,
            tax_redistributed=0.0,
            attention_spread=0.0,
            gini_coefficient=gini,
        )

    @staticmethod
    def _gini_coefficient(values: List[float]) -> float:
        """Compute Gini coefficient measuring inequality."""
        sorted_vals = sorted(max(0, v) for v in values)
        n = len(sorted_vals)
        if n == 0:
            return 0.0
        total = sum(sorted_vals)
        if total == 0:
            return 0.0
        cumulative = 0.0
        gini_sum = 0.0
        for i, val in enumerate(sorted_vals):
            cumulative += val
            gini_sum += (2 * (i + 1) - n - 1) * val
        return gini_sum / (n * total)


def run_simulation(num_atoms: int = 200, num_cycles: int = 500,
                   seed: int = 42) -> Dict:
    """Run a full ECAN simulation and return results."""
    config = ECANConfig()
    sim = ECANSimulator(config, num_atoms=num_atoms, seed=seed)

    start_time = time.time()
    for cycle in range(num_cycles):
        sim.run_cycle(cycle)
    elapsed = time.time() - start_time

    # Validate convergence: STI std should stabilize
    last_50_std = [m.std_sti for m in sim.cycle_history[-50:]]
    std_of_std = (sum((s - sum(last_50_std) / len(last_50_std)) ** 2
                      for s in last_50_std) / len(last_50_std)) ** 0.5

    # Validate budget conservation
    budget_deviation = abs(
        sim.cycle_history[-1].total_sti - config.total_sti_budget
    ) / config.total_sti_budget

    results = {
        "simulation_params": {
            "num_atoms": num_atoms,
            "num_cycles": num_cycles,
            "seed": seed,
            "config": asdict(config) if hasattr(config, '__dataclass_fields__') else vars(config),
        },
        "performance": {
            "total_time_s": elapsed,
            "time_per_cycle_ms": (elapsed / num_cycles) * 1000,
            "cycles_per_second": num_cycles / elapsed,
        },
        "final_state": {
            "total_sti": sim.cycle_history[-1].total_sti,
            "mean_sti": sim.cycle_history[-1].mean_sti,
            "std_sti": sim.cycle_history[-1].std_sti,
            "gini_coefficient": sim.cycle_history[-1].gini_coefficient,
            "atoms_in_focus": sim.cycle_history[-1].atoms_in_focus,
        },
        "convergence": {
            "std_of_std_last_50": std_of_std,
            "converged": std_of_std < 5.0,
            "budget_deviation_pct": budget_deviation * 100,
            "budget_conserved": budget_deviation < 0.1,
        },
        "validation": {
            "rent_collected_total": sum(m.rent_collected for m in sim.cycle_history),
            "wages_paid_total": sum(m.wages_paid for m in sim.cycle_history),
            "tax_redistributed_total": sum(m.tax_redistributed for m in sim.cycle_history),
            "attention_spread_total": sum(m.attention_spread for m in sim.cycle_history),
        },
        "time_series_sample": [asdict(m) for m in sim.cycle_history[::50]],
    }

    return results


def test_ecan_simulation():
    """Main test: Run ECAN simulation and validate results."""
    print("=" * 70)
    print("ECAN Attention Simulation Test")
    print("Issue #218: Cognitive Layer — Distributed Cognition Dynamics")
    print("=" * 70)

    results = run_simulation(num_atoms=200, num_cycles=500, seed=42)

    # Print summary
    print(f"\nSimulation: {results['simulation_params']['num_atoms']} atoms, "
          f"{results['simulation_params']['num_cycles']} cycles")
    print(f"Time: {results['performance']['total_time_s']:.3f}s "
          f"({results['performance']['time_per_cycle_ms']:.2f} ms/cycle)")
    print(f"\nFinal State:")
    print(f"  Total STI: {results['final_state']['total_sti']:.2f}")
    print(f"  Mean STI: {results['final_state']['mean_sti']:.2f}")
    print(f"  Std STI: {results['final_state']['std_sti']:.2f}")
    print(f"  Gini: {results['final_state']['gini_coefficient']:.4f}")
    print(f"  Atoms in focus: {results['final_state']['atoms_in_focus']}")
    print(f"\nConvergence:")
    print(f"  Converged: {results['convergence']['converged']}")
    print(f"  Budget deviation: {results['convergence']['budget_deviation_pct']:.2f}%")
    print(f"  Budget conserved: {results['convergence']['budget_conserved']}")

    # Assertions
    assert results['convergence']['budget_conserved'], \
        f"Budget not conserved: {results['convergence']['budget_deviation_pct']:.2f}% deviation"
    assert results['final_state']['gini_coefficient'] < 1.0, \
        "Gini coefficient should be < 1.0 (not total inequality)"
    assert results['final_state']['gini_coefficient'] > 0.0, \
        "Gini coefficient should be > 0.0 (some differentiation expected)"
    assert results['validation']['rent_collected_total'] > 0, \
        "Rent should be collected"
    assert results['validation']['wages_paid_total'] > 0, \
        "Wages should be paid"
    assert results['validation']['attention_spread_total'] > 0, \
        "Attention should spread"

    print("\n✓ All ECAN simulation assertions passed")

    # Write JSON output
    output_path = "test_ecan_simulation_results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults written to: {output_path}")

    return results


if __name__ == "__main__":
    test_ecan_simulation()
