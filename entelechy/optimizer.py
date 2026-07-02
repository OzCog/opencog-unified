"""
Entelechy Optimizer

Evolutionary optimization for iterative entelechy improvement.
Implements gradient ascent on the fitness landscape.
"""

from collections.abc import Callable
from pathlib import Path

from .genome import EntelechyGenome
from .introspector import EntelechyIntrospector
from .types import EntelechyDimension, EntelechyMetrics


class EntelechyOptimizer:
    """
    Optimize system entelechy through iterative refinement

    Implements optimization algorithms for improving actualization
    through targeted dimensional improvements.
    """

    def __init__(self, repo_path: str, learning_rate: float = 0.1):
        """
        Initialize optimizer

        Args:
            repo_path: Path to repository
            learning_rate: Learning rate for optimization (default: 0.1)
        """
        self.repo_path = Path(repo_path).resolve()
        self.learning_rate = learning_rate
        self.evolution_history = []
        self.current_genome = None

    def optimize(self, iterations: int, improvement_callback: Callable | None = None) -> dict:
        """
        Optimize system entelechy through iterative refinement

        Args:
            iterations: Number of optimization iterations
            improvement_callback: Optional callback function for applying improvements

        Returns:
            Dictionary with optimization results
        """
        print(f"🎯 Starting Entelechy Optimization ({iterations} iterations)")
        print("=" * 70)

        for i in range(iterations):
            print(f"\n📈 Iteration {i + 1}/{iterations}")

            # Assess current state
            introspector = EntelechyIntrospector(str(self.repo_path))
            introspector.perform_deep_introspection()
            metrics = introspector.metrics

            # Create/evolve genome
            if self.current_genome is None:
                self.current_genome = EntelechyGenome.from_metrics(metrics)
            else:
                self.current_genome = self.current_genome.evolve(metrics)

            # Identify weakest dimension
            weakest_dim, weakest_score = self._identify_weakest_dimension(metrics)

            print(f"  Weakest dimension: {weakest_dim.value} ({weakest_score:.2%})")

            # Generate improvements for weakest dimension
            improvements = self.generate_improvements(weakest_dim, metrics)

            print(f"  Generated {len(improvements)} improvement suggestions")

            # Apply improvements if callback provided
            if improvement_callback:
                print("  Applying improvements...")
                applied = improvement_callback(weakest_dim, improvements)
                print(f"  Applied {applied} improvements")

            # Record iteration in history
            fitness_gain = metrics.fitness() - (
                self.evolution_history[-1]["fitness"] if self.evolution_history else 0.0
            )

            self.evolution_history.append(
                {
                    "iteration": i,
                    "actualization": metrics.actualization_score,
                    "fitness": metrics.fitness(),
                    "dimension_improved": weakest_dim.value,
                    "fitness_gain": fitness_gain,
                    "improvements_generated": len(improvements),
                    "genome_id": self.current_genome.id,
                }
            )

        # Generate optimization report
        return self._generate_optimization_report()

    def generate_improvements(self, dimension: EntelechyDimension, metrics: EntelechyMetrics) -> list[dict]:
        """
        Generate targeted improvements for a dimension

        Args:
            dimension: Dimension to improve
            metrics: Current metrics

        Returns:
            List of improvement actions
        """
        improvements = []

        if dimension == EntelechyDimension.ONTOLOGICAL:
            improvements.extend(self._generate_ontological_improvements(metrics))
        elif dimension == EntelechyDimension.TELEOLOGICAL:
            improvements.extend(self._generate_teleological_improvements(metrics))
        elif dimension == EntelechyDimension.COGNITIVE:
            improvements.extend(self._generate_cognitive_improvements(metrics))
        elif dimension == EntelechyDimension.INTEGRATIVE:
            improvements.extend(self._generate_integrative_improvements(metrics))
        elif dimension == EntelechyDimension.EVOLUTIONARY:
            improvements.extend(self._generate_evolutionary_improvements(metrics))

        return improvements

    def _identify_weakest_dimension(self, metrics: EntelechyMetrics) -> tuple:
        """
        Identify weakest dimensional score

        Args:
            metrics: Current metrics

        Returns:
            Tuple of (dimension, score)
        """
        dimensions = {
            EntelechyDimension.ONTOLOGICAL: metrics.completeness_score,
            EntelechyDimension.TELEOLOGICAL: metrics.alignment_score,
            EntelechyDimension.COGNITIVE: metrics.actualization_score,
            EntelechyDimension.INTEGRATIVE: metrics.coherence_score,
            EntelechyDimension.EVOLUTIONARY: metrics.vitality_score,
        }

        weakest = min(dimensions.items(), key=lambda x: x[1])
        return weakest

    def _generate_ontological_improvements(self, metrics: EntelechyMetrics) -> list[dict]:
        """Generate improvements for ontological dimension"""
        improvements = []

        if metrics.completeness_score < 0.9:
            improvements.append(
                {
                    "action": "complete_missing_components",
                    "priority": "high",
                    "description": "Integrate missing architectural components",
                    "expected_gain": 0.1,
                }
            )

        improvements.append(
            {
                "action": "strengthen_foundation",
                "priority": "medium",
                "description": "Enhance core utilities and foundation layer",
                "expected_gain": 0.05,
            }
        )

        return improvements

    def _generate_teleological_improvements(self, metrics: EntelechyMetrics) -> list[dict]:
        """Generate improvements for teleological dimension"""
        improvements = []

        improvements.append(
            {
                "action": "refine_roadmap",
                "priority": "high",
                "description": "Update and refine development roadmap",
                "expected_gain": 0.08,
            }
        )

        improvements.append(
            {
                "action": "clarify_goals",
                "priority": "medium",
                "description": "Document and clarify system goals and purpose",
                "expected_gain": 0.05,
            }
        )

        return improvements

    def _generate_cognitive_improvements(self, metrics: EntelechyMetrics) -> list[dict]:
        """Generate improvements for cognitive dimension"""
        improvements = []

        improvements.append(
            {
                "action": "enhance_reasoning",
                "priority": "high",
                "description": "Strengthen PLN and URE reasoning systems",
                "expected_gain": 0.1,
            }
        )

        improvements.append(
            {
                "action": "optimize_learning",
                "priority": "medium",
                "description": "Improve MOSES and learning algorithms",
                "expected_gain": 0.07,
            }
        )

        return improvements

    def _generate_integrative_improvements(self, metrics: EntelechyMetrics) -> list[dict]:
        """Generate improvements for integrative dimension"""
        improvements = []

        improvements.append(
            {
                "action": "strengthen_dependencies",
                "priority": "high",
                "description": "Resolve dependency issues and strengthen linkages",
                "expected_gain": 0.09,
            }
        )

        improvements.append(
            {
                "action": "expand_tests",
                "priority": "medium",
                "description": "Expand test coverage and integration testing",
                "expected_gain": 0.06,
            }
        )

        return improvements

    def _generate_evolutionary_improvements(self, metrics: EntelechyMetrics) -> list[dict]:
        """Generate improvements for evolutionary dimension"""
        improvements = []

        if metrics.total_code_markers > 1000:
            improvements.append(
                {
                    "action": "resolve_markers",
                    "priority": "critical",
                    "description": f"Resolve {metrics.total_code_markers} TODO/FIXME/STUB markers",
                    "expected_gain": 0.15,
                }
            )

        improvements.append(
            {
                "action": "enhance_meta_tools",
                "priority": "medium",
                "description": "Develop additional meta-cognitive tools",
                "expected_gain": 0.05,
            }
        )

        return improvements

    def _generate_optimization_report(self) -> dict:
        """Generate comprehensive optimization report"""
        if not self.evolution_history:
            return {"status": "no_history"}

        first = self.evolution_history[0]
        last = self.evolution_history[-1]

        total_fitness_gain = last["fitness"] - first["fitness"]
        total_actualization_gain = last["actualization"] - first["actualization"]

        # Calculate average improvement per iteration
        avg_fitness_gain = total_fitness_gain / len(self.evolution_history)

        # Identify most improved dimension
        dimension_improvements = {}
        for record in self.evolution_history:
            dim = record["dimension_improved"]
            dimension_improvements[dim] = dimension_improvements.get(dim, 0) + 1

        most_improved = max(dimension_improvements.items(), key=lambda x: x[1])[0]

        return {
            "status": "complete",
            "total_iterations": len(self.evolution_history),
            "initial_fitness": first["fitness"],
            "final_fitness": last["fitness"],
            "total_fitness_gain": total_fitness_gain,
            "initial_actualization": first["actualization"],
            "final_actualization": last["actualization"],
            "total_actualization_gain": total_actualization_gain,
            "avg_fitness_gain_per_iteration": avg_fitness_gain,
            "most_improved_dimension": most_improved,
            "dimension_improvement_counts": dimension_improvements,
            "evolution_history": self.evolution_history,
            "final_genome_id": self.current_genome.id if self.current_genome else None,
        }
