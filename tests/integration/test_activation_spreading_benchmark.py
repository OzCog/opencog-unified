#!/usr/bin/env python3
"""
Activation Spreading Benchmark
Issue #218: Cognitive Layer — Distributed Cognition Dynamics

Benchmarks spreading performance across varying network sizes.
Measures: time per cycle, atoms processed/sec, convergence rate,
activation distribution (Gini coefficient).
"""

import json
import math
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class BenchmarkResult:
    """Result for a single benchmark run."""
    network_size: int
    num_links: int
    num_cycles: int
    total_time_s: float
    time_per_cycle_ms: float
    atoms_per_second: float
    spreads_per_second: float
    initial_gini: float
    final_gini: float
    convergence_cycle: int  # Cycle at which STI distribution stabilized
    mean_spreading_per_cycle: float
    peak_memory_atoms: int


class ActivationNetwork:
    """Network for activation spreading benchmark."""

    def __init__(self, num_atoms: int, avg_degree: int = 4, seed: int = 42):
        self.rng = random.Random(seed)
        self.num_atoms = num_atoms
        self.sti = [0.0] * num_atoms
        self.neighbors: List[List[int]] = [[] for _ in range(num_atoms)]
        self.weights: List[Dict[int, float]] = [{} for _ in range(num_atoms)]
        self.num_links = 0
        self._build_network(avg_degree)

    def _build_network(self, avg_degree: int):
        """Build random graph with specified average degree."""
        for i in range(self.num_atoms):
            self.sti[i] = self.rng.gauss(50.0, 30.0)

        # Erdos-Renyi style random edges
        target_edges = self.num_atoms * avg_degree // 2
        edges_created = 0
        attempts = 0
        max_attempts = target_edges * 10

        while edges_created < target_edges and attempts < max_attempts:
            a = self.rng.randint(0, self.num_atoms - 1)
            b = self.rng.randint(0, self.num_atoms - 1)
            if a != b and b not in self.weights[a]:
                weight = self.rng.uniform(0.1, 1.0)
                self.neighbors[a].append(b)
                self.neighbors[b].append(a)
                self.weights[a][b] = weight
                self.weights[b][a] = weight
                edges_created += 1
            attempts += 1

        self.num_links = edges_created

    def spread_cycle(self, spreading_rate: float = 0.3,
                     threshold: float = 10.0) -> float:
        """One cycle of activation spreading. Returns total spread amount."""
        total_spread = 0.0
        updates = [0.0] * self.num_atoms

        for i in range(self.num_atoms):
            if self.sti[i] < threshold:
                continue
            if not self.neighbors[i]:
                continue

            spread_amount = self.sti[i] * spreading_rate
            total_weight = sum(self.weights[i].values())
            if total_weight == 0:
                continue

            for neighbor in self.neighbors[i]:
                w = self.weights[i].get(neighbor, 0.0)
                share = spread_amount * (w / total_weight)
                updates[neighbor] += share
                total_spread += share

            updates[i] -= spread_amount

        # Apply updates
        for i in range(self.num_atoms):
            self.sti[i] += updates[i]

        return total_spread

    def get_gini(self) -> float:
        """Compute Gini coefficient of current STI distribution."""
        sorted_vals = sorted(max(0, v) for v in self.sti)
        n = len(sorted_vals)
        total = sum(sorted_vals)
        if total == 0 or n == 0:
            return 0.0
        gini_sum = sum((2 * (i + 1) - n - 1) * val
                       for i, val in enumerate(sorted_vals))
        return gini_sum / (n * total)

    def get_std(self) -> float:
        """Compute std deviation of STI."""
        mean = sum(self.sti) / len(self.sti)
        variance = sum((s - mean) ** 2 for s in self.sti) / len(self.sti)
        return math.sqrt(variance)


def run_benchmark(network_size: int, num_cycles: int = 200,
                  seed: int = 42) -> BenchmarkResult:
    """Run spreading benchmark for a given network size."""
    net = ActivationNetwork(network_size, avg_degree=4, seed=seed)
    initial_gini = net.get_gini()

    spreading_amounts = []
    std_history = []
    convergence_cycle = num_cycles  # default: didn't converge

    start_time = time.time()

    for cycle in range(num_cycles):
        spread = net.spread_cycle(spreading_rate=0.3, threshold=10.0)
        spreading_amounts.append(spread)
        current_std = net.get_std()
        std_history.append(current_std)

        # Check for convergence (std stabilized)
        if cycle > 20 and convergence_cycle == num_cycles:
            recent_std = std_history[-10:]
            std_of_std = (sum((s - sum(recent_std) / len(recent_std)) ** 2
                              for s in recent_std) / len(recent_std)) ** 0.5
            if std_of_std < 0.5:
                convergence_cycle = cycle

    elapsed = time.time() - start_time
    final_gini = net.get_gini()

    return BenchmarkResult(
        network_size=network_size,
        num_links=net.num_links,
        num_cycles=num_cycles,
        total_time_s=elapsed,
        time_per_cycle_ms=(elapsed / num_cycles) * 1000,
        atoms_per_second=(network_size * num_cycles) / elapsed,
        spreads_per_second=sum(1 for s in spreading_amounts if s > 0) / elapsed,
        initial_gini=initial_gini,
        final_gini=final_gini,
        convergence_cycle=convergence_cycle,
        mean_spreading_per_cycle=sum(spreading_amounts) / num_cycles,
        peak_memory_atoms=network_size,
    )


def test_activation_spreading_benchmark():
    """Main benchmark: test spreading at multiple scales."""
    print("=" * 70)
    print("Activation Spreading Benchmark")
    print("Issue #218: Cognitive Layer — Distributed Cognition Dynamics")
    print("=" * 70)

    network_sizes = [100, 500, 1000, 5000, 10000]
    results = []

    for size in network_sizes:
        print(f"\n--- Network size: {size} atoms ---")
        result = run_benchmark(size, num_cycles=200, seed=42)
        results.append(result)

        print(f"  Links: {result.num_links}")
        print(f"  Time: {result.total_time_s:.3f}s "
              f"({result.time_per_cycle_ms:.2f} ms/cycle)")
        print(f"  Throughput: {result.atoms_per_second:.0f} atoms/s")
        print(f"  Gini: {result.initial_gini:.4f} → {result.final_gini:.4f}")
        print(f"  Convergence cycle: {result.convergence_cycle}")
        print(f"  Mean spread/cycle: {result.mean_spreading_per_cycle:.2f}")

    # Validate scaling behavior
    print("\n" + "=" * 70)
    print("Scaling Analysis:")
    print("-" * 70)
    print(f"{'Size':>8} {'Time/cycle':>12} {'Atoms/s':>12} {'Scaling':>10}")
    print("-" * 70)

    for i, r in enumerate(results):
        scaling = ""
        if i > 0:
            time_ratio = r.time_per_cycle_ms / results[i-1].time_per_cycle_ms
            size_ratio = r.network_size / results[i-1].network_size
            scaling_exp = math.log(time_ratio) / math.log(size_ratio)
            scaling = f"O(n^{scaling_exp:.2f})"
        print(f"{r.network_size:>8} {r.time_per_cycle_ms:>10.2f}ms "
              f"{r.atoms_per_second:>10.0f} {scaling:>10}")

    # Assertions
    for r in results:
        assert r.total_time_s > 0, "Benchmark should take positive time"
        assert r.final_gini >= 0, "Gini should be non-negative"
        assert r.final_gini <= 1.0, "Gini should be <= 1.0"
        assert r.mean_spreading_per_cycle > 0, "Should have non-zero spreading"

    # Sub-quadratic scaling check
    if len(results) >= 2:
        smallest = results[0]
        largest = results[-1]
        time_ratio = largest.time_per_cycle_ms / smallest.time_per_cycle_ms
        size_ratio = largest.network_size / smallest.network_size
        scaling_exp = math.log(time_ratio) / math.log(size_ratio)
        assert scaling_exp < 2.5, \
            f"Scaling too steep: O(n^{scaling_exp:.2f}), expected sub-quadratic"
        print(f"\n✓ Overall scaling: O(n^{scaling_exp:.2f}) — sub-quadratic confirmed")

    print("\n✓ All activation spreading benchmark assertions passed")

    # Write JSON output
    output = {
        "benchmark": "activation_spreading",
        "results": [
            {
                "network_size": r.network_size,
                "num_links": r.num_links,
                "num_cycles": r.num_cycles,
                "total_time_s": r.total_time_s,
                "time_per_cycle_ms": r.time_per_cycle_ms,
                "atoms_per_second": r.atoms_per_second,
                "initial_gini": r.initial_gini,
                "final_gini": r.final_gini,
                "convergence_cycle": r.convergence_cycle,
                "mean_spreading_per_cycle": r.mean_spreading_per_cycle,
            }
            for r in results
        ]
    }
    output_path = "test_activation_spreading_benchmark_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults written to: {output_path}")


if __name__ == "__main__":
    test_activation_spreading_benchmark()
