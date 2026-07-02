#!/usr/bin/env python3
"""
Attention Spreading Benchmarks for Phase 2 ECAN

Benchmarks the attention spreading algorithms across distributed agents
with performance analysis under high cognitive load.
"""

import random
import statistics
import time


class AttentionSpreadingBenchmarks:
    """Benchmark suite for attention spreading performance"""

    def __init__(self):
        self.benchmark_results = {}

    def setup_test_environment(self, num_atoms=1000, num_agents=5):
        """Set up benchmark test environment"""
        print(f"Setting up benchmark: {num_atoms} atoms, {num_agents} agents")

        # Simulate atom network
        self.atoms = []
        for i in range(num_atoms):
            atom = {
                "id": f"atom_{i}",
                "attention_value": random.uniform(0, 100),
                "connections": random.sample(range(num_atoms), min(10, num_atoms - 1)),
            }
            self.atoms.append(atom)

        # Simulate distributed agents
        self.agents = []
        for i in range(num_agents):
            agent = {
                "id": f"agent_{i}",
                "focus_atoms": random.sample(range(num_atoms), min(50, num_atoms)),
                "spreading_rate": random.uniform(0.05, 0.15),
                "processing_capacity": random.uniform(100, 500),  # atoms per cycle
            }
            self.agents.append(agent)

        print(
            f"✓ Created {len(self.atoms)} atoms with avg {statistics.mean([len(a['connections']) for a in self.atoms]):.1f} connections"
        )
        print(
            f"✓ Created {len(self.agents)} agents with avg {statistics.mean([len(a['focus_atoms']) for a in self.agents]):.1f} focus atoms"
        )

    def benchmark_single_agent_spreading(self, cycles=100):
        """Benchmark attention spreading within single agent"""
        print(f"\n=== Single Agent Spreading Benchmark ({cycles} cycles) ===")

        agent = self.agents[0]
        start_time = time.time()
        spreads_performed = 0

        for _cycle in range(cycles):
            # Simulate attention spreading for one agent
            focus_atoms = agent["focus_atoms"][: int(agent["processing_capacity"])]

            for atom_idx in focus_atoms:
                atom = self.atoms[atom_idx]

                # Spread to connected atoms
                for connected_idx in atom["connections"][:3]:  # Limit spreading
                    if connected_idx < len(self.atoms):
                        source_attention = atom["attention_value"]
                        target_attention = self.atoms[connected_idx]["attention_value"]

                        if source_attention > target_attention:
                            spread_amount = (source_attention - target_attention) * agent["spreading_rate"]
                            atom["attention_value"] -= spread_amount * 0.1
                            self.atoms[connected_idx]["attention_value"] += spread_amount * 0.1
                            spreads_performed += 1

        elapsed_time = time.time() - start_time
        spreads_per_second = spreads_performed / elapsed_time

        print(f"✓ Performed {spreads_performed} spreads in {elapsed_time:.3f}s")
        print(f"✓ Spreading rate: {spreads_per_second:.0f} spreads/second")
        print(f"✓ Average cycle time: {elapsed_time / cycles * 1000:.2f}ms")

        self.benchmark_results["single_agent_spreads_per_second"] = spreads_per_second
        self.benchmark_results["single_agent_cycle_time"] = elapsed_time / cycles * 1000

        return spreads_per_second

    def benchmark_multi_agent_spreading(self, cycles=50):
        """Benchmark attention spreading across multiple agents"""
        print(f"\n=== Multi-Agent Spreading Benchmark ({cycles} cycles) ===")

        start_time = time.time()
        total_spreads = 0
        sync_operations = 0

        for cycle in range(cycles):
            agent_spreads = []

            # Each agent processes independently
            for agent in self.agents:
                agent_start = time.time()
                spreads = 0

                focus_atoms = agent["focus_atoms"][: int(agent["processing_capacity"] / len(self.agents))]

                for atom_idx in focus_atoms:
                    if atom_idx < len(self.atoms):
                        atom = self.atoms[atom_idx]

                        # Spread within agent's focus
                        for connected_idx in atom["connections"][:2]:
                            if connected_idx < len(self.atoms) and connected_idx in focus_atoms:
                                source_attention = atom["attention_value"]
                                target_attention = self.atoms[connected_idx]["attention_value"]

                                if source_attention > target_attention:
                                    spread_amount = (source_attention - target_attention) * agent["spreading_rate"]
                                    atom["attention_value"] -= spread_amount * 0.1
                                    self.atoms[connected_idx]["attention_value"] += spread_amount * 0.1
                                    spreads += 1

                agent_time = time.time() - agent_start
                agent_spreads.append({"agent": agent["id"], "spreads": spreads, "time": agent_time})
                total_spreads += spreads

            # Simulate inter-agent synchronization
            if cycle % 10 == 0:  # Sync every 10 cycles
                sync_start = time.time()

                # High attention atoms get shared between agents
                high_attention_atoms = [i for i, atom in enumerate(self.atoms) if atom["attention_value"] > 80]

                for agent in self.agents:
                    # Share top atoms with other agents
                    shared_atoms = random.sample(high_attention_atoms, min(5, len(high_attention_atoms)))
                    for other_agent in self.agents:
                        if other_agent != agent:
                            # Simulate attention sync message
                            sync_operations += len(shared_atoms)

                time.time() - sync_start

        elapsed_time = time.time() - start_time
        total_spreads_per_second = total_spreads / elapsed_time
        sync_ops_per_second = sync_operations / elapsed_time

        print(f"✓ Total spreads: {total_spreads} across {len(self.agents)} agents")
        print(f"✓ Sync operations: {sync_operations}")
        print(f"✓ Multi-agent spreading rate: {total_spreads_per_second:.0f} spreads/second")
        print(f"✓ Sync rate: {sync_ops_per_second:.0f} sync ops/second")
        print(f"✓ Average cycle time: {elapsed_time / cycles * 1000:.2f}ms")

        self.benchmark_results["multi_agent_spreads_per_second"] = total_spreads_per_second
        self.benchmark_results["sync_ops_per_second"] = sync_ops_per_second
        self.benchmark_results["multi_agent_cycle_time"] = elapsed_time / cycles * 1000

        return total_spreads_per_second

    def benchmark_high_load_performance(self, load_multiplier=5):
        """Benchmark performance under high cognitive load"""
        print(f"\n=== High Load Performance Benchmark (load x{load_multiplier}) ===")

        # Increase system load
        original_focus_sizes = [len(agent["focus_atoms"]) for agent in self.agents]
        for agent in self.agents:
            agent["focus_atoms"] = random.sample(
                range(len(self.atoms)), min(len(agent["focus_atoms"]) * load_multiplier, len(self.atoms))
            )

        # Benchmark under load
        start_time = time.time()
        cycles = 20  # Fewer cycles due to higher load

        total_operations = 0
        memory_usage_sim = 0  # Simulated memory usage

        for _cycle in range(cycles):
            cycle_operations = 0

            for agent in self.agents:
                # Process larger attention sets
                for atom_idx in agent["focus_atoms"]:
                    if atom_idx < len(self.atoms):
                        atom = self.atoms[atom_idx]

                        # Simulate more complex attention calculations
                        attention_complexity = len(atom["connections"]) * atom["attention_value"]
                        memory_usage_sim += attention_complexity * 0.001  # KB

                        # Perform spreading operations
                        for connected_idx in atom["connections"]:
                            if connected_idx < len(self.atoms):
                                cycle_operations += 1

                                # Simulate computational cost
                                _ = atom["attention_value"] * random.uniform(0.9, 1.1)

            total_operations += cycle_operations

        elapsed_time = time.time() - start_time
        operations_per_second = total_operations / elapsed_time

        print(f"✓ High load operations: {total_operations}")
        print(f"✓ Operations per second: {operations_per_second:.0f}")
        print(f"✓ Simulated memory usage: {memory_usage_sim / 1024:.2f} MB")
        print(f"✓ Average high load cycle: {elapsed_time / cycles * 1000:.2f}ms")

        # Performance degradation analysis
        baseline_ops = self.benchmark_results.get("single_agent_spreads_per_second", 1000)
        performance_ratio = operations_per_second / (baseline_ops * load_multiplier)

        print(f"✓ Performance efficiency under load: {performance_ratio:.1%}")

        # Restore original focus sizes
        for i, agent in enumerate(self.agents):
            agent["focus_atoms"] = random.sample(range(len(self.atoms)), original_focus_sizes[i])

        self.benchmark_results["high_load_ops_per_second"] = operations_per_second
        self.benchmark_results["high_load_performance_ratio"] = performance_ratio
        self.benchmark_results["memory_usage_mb"] = memory_usage_sim / 1024

        return operations_per_second

    def benchmark_attention_fairness(self):
        """Benchmark attention allocation fairness across agents"""
        print("\n=== Attention Fairness Benchmark ===")

        # Calculate initial attention distribution
        initial_distribution = {}
        for _i, agent in enumerate(self.agents):
            agent_total_attention = sum(
                self.atoms[idx]["attention_value"] for idx in agent["focus_atoms"] if idx < len(self.atoms)
            )
            initial_distribution[agent["id"]] = agent_total_attention

        # Run fairness-oriented spreading
        cycles = 30
        fairness_scores = []

        for _cycle in range(cycles):
            # Calculate current distribution
            current_distribution = {}
            for agent in self.agents:
                agent_total_attention = sum(
                    self.atoms[idx]["attention_value"] for idx in agent["focus_atoms"] if idx < len(self.atoms)
                )
                current_distribution[agent["id"]] = agent_total_attention

            # Calculate Gini coefficient for fairness
            values = list(current_distribution.values())
            if values:
                sorted_values = sorted(values)
                n = len(sorted_values)
                index = list(range(1, n + 1))
                gini = (2 * sum(index[i] * sorted_values[i] for i in range(n))) / (n * sum(sorted_values)) - (n + 1) / n
                fairness_score = 1.0 - gini
                fairness_scores.append(fairness_score)

            # Apply fairness-oriented redistribution
            mean_attention = statistics.mean(values) if values else 0
            for agent in self.agents:
                agent_attention = current_distribution.get(agent["id"], 0)

                if agent_attention < mean_attention * 0.8:  # Below fair share
                    # Boost low-attention agents
                    for atom_idx in random.sample(agent["focus_atoms"], min(5, len(agent["focus_atoms"]))):
                        if atom_idx < len(self.atoms):
                            self.atoms[atom_idx]["attention_value"] += 2.0
                elif agent_attention > mean_attention * 1.2:  # Above fair share
                    # Reduce high-attention agents slightly
                    for atom_idx in random.sample(agent["focus_atoms"], min(3, len(agent["focus_atoms"]))):
                        if atom_idx < len(self.atoms):
                            self.atoms[atom_idx]["attention_value"] *= 0.98

        average_fairness = statistics.mean(fairness_scores) if fairness_scores else 0
        fairness_improvement = fairness_scores[-1] - fairness_scores[0] if len(fairness_scores) > 1 else 0

        print(f"✓ Average fairness score: {average_fairness:.3f}")
        print(f"✓ Fairness improvement: {fairness_improvement:+.3f}")
        print("✓ Final agent distributions:")

        final_distribution = {}
        for agent in self.agents:
            agent_total_attention = sum(
                self.atoms[idx]["attention_value"] for idx in agent["focus_atoms"] if idx < len(self.atoms)
            )
            final_distribution[agent["id"]] = agent_total_attention
            print(f"  {agent['id']}: {agent_total_attention:.1f}")

        self.benchmark_results["attention_fairness_score"] = average_fairness
        self.benchmark_results["fairness_improvement"] = fairness_improvement

        return average_fairness

    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        print(f"\n{'=' * 60}")
        print("ATTENTION SPREADING PERFORMANCE REPORT")
        print(f"{'=' * 60}")

        # Performance summary
        print("\n📊 PERFORMANCE METRICS:")
        for metric, value in self.benchmark_results.items():
            if "per_second" in metric:
                print(f"  {metric.replace('_', ' ').title()}: {value:,.0f}")
            elif "time" in metric:
                print(f"  {metric.replace('_', ' ').title()}: {value:.2f}ms")
            elif "ratio" in metric or "score" in metric or "improvement" in metric:
                print(f"  {metric.replace('_', ' ').title()}: {value:.3f}")
            elif "mb" in metric.lower():
                print(f"  {metric.replace('_', ' ').title()}: {value:.2f}MB")

        # Performance analysis
        single_agent_rate = self.benchmark_results.get("single_agent_spreads_per_second", 0)
        multi_agent_rate = self.benchmark_results.get("multi_agent_spreads_per_second", 0)

        if single_agent_rate > 0:
            scaling_efficiency = multi_agent_rate / (single_agent_rate * len(self.agents))
            print("\n📈 SCALING ANALYSIS:")
            print(f"  Multi-agent scaling efficiency: {scaling_efficiency:.1%}")

        # Fairness analysis
        fairness_score = self.benchmark_results.get("attention_fairness_score", 0)
        if fairness_score > 0:
            print("\n⚖️ FAIRNESS ANALYSIS:")
            print(
                f"  Overall fairness rating: {'Excellent' if fairness_score > 0.8 else 'Good' if fairness_score > 0.6 else 'Fair'}"
            )

        # Performance rating
        high_load_ratio = self.benchmark_results.get("high_load_performance_ratio", 0)
        if high_load_ratio > 0:
            print("\n🚀 PERFORMANCE RATING:")
            rating = "Excellent" if high_load_ratio > 0.8 else "Good" if high_load_ratio > 0.6 else "Needs Improvement"
            print(f"  Under high load: {rating} ({high_load_ratio:.1%} efficiency)")

        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        if scaling_efficiency < 0.7:
            print("  • Optimize inter-agent synchronization to improve scaling")
        if fairness_score < 0.7:
            print("  • Implement stronger fairness mechanisms")
        if high_load_ratio < 0.6:
            print("  • Consider attention pruning under high load")
        if multi_agent_rate < 1000:
            print("  • Optimize attention spreading algorithms")

        print("\n✅ Benchmark completed successfully!")


def main():
    """Run attention spreading benchmarks"""
    print("Phase 2 ECAN Attention Spreading Benchmarks")
    print("=" * 50)

    # Initialize benchmark suite
    benchmarks = AttentionSpreadingBenchmarks()

    # Set up test environment
    benchmarks.setup_test_environment(num_atoms=500, num_agents=3)

    # Run benchmark suite
    print("\n🔄 Running benchmark suite...")

    benchmarks.benchmark_single_agent_spreading(cycles=50)
    benchmarks.benchmark_multi_agent_spreading(cycles=30)
    benchmarks.benchmark_high_load_performance(load_multiplier=3)
    benchmarks.benchmark_attention_fairness()

    # Generate final report
    benchmarks.generate_performance_report()


if __name__ == "__main__":
    main()
