"""
Entelechy Genome

The "DNA" of the cognitive system - tracks genetic configuration
and evolutionary lineage of the system's entelechy.
"""

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime

from .types import EntelechyMetrics


@dataclass
class EntelechyGenome:
    """
    Entelechy Genome: The "DNA" of the cognitive system

    Tracks the genetic configuration and evolutionary lineage
    of the system's vital actualization.
    """
    id: str
    generation: int
    lineage: list[str] = field(default_factory=list)

    # Genetic material (dimensional genes)
    genes: dict[str, list[float]] = field(default_factory=lambda: {
        'ontological': [],
        'teleological': [],
        'cognitive': [],
        'integrative': [],
        'evolutionary': [],
    })

    # Fitness and maturity
    fitness: float = 0.0
    age: int = 0  # Number of iterations/generations
    actualization_level: float = 0.0

    # Timestamps
    birth_time: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    last_update: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')

    @classmethod
    def from_metrics(cls, metrics: EntelechyMetrics, parent_genome: 'EntelechyGenome' = None) -> 'EntelechyGenome':
        """
        Create genome from entelechy metrics

        Args:
            metrics: Current entelechy metrics
            parent_genome: Optional parent genome for lineage tracking

        Returns:
            New EntelechyGenome instance
        """
        # Generate unique ID
        genome_id = cls._generate_id(metrics)

        # Determine generation and lineage
        if parent_genome:
            generation = parent_genome.generation + 1
            lineage = [*parent_genome.lineage, parent_genome.id]
        else:
            generation = 0
            lineage = []

        # Extract genes from metrics
        genes = {
            'ontological': [metrics.completeness_score],
            'teleological': [metrics.alignment_score],
            'cognitive': [metrics.actualization_score],
            'integrative': [metrics.coherence_score],
            'evolutionary': [metrics.vitality_score],
        }

        return cls(
            id=genome_id,
            generation=generation,
            lineage=lineage,
            genes=genes,
            fitness=metrics.fitness(),
            actualization_level=metrics.actualization_score,
            age=0
        )

    @staticmethod
    def _generate_id(metrics: EntelechyMetrics) -> str:
        """Generate unique genome ID from metrics"""
        timestamp = datetime.utcnow().isoformat()
        data = f"{timestamp}:{metrics.actualization_score}:{metrics.fitness()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def evolve(self, new_metrics: EntelechyMetrics) -> 'EntelechyGenome':
        """
        Evolve genome to next generation

        Args:
            new_metrics: Updated entelechy metrics

        Returns:
            New evolved genome
        """
        return EntelechyGenome.from_metrics(new_metrics, parent_genome=self)

    def mutate(self, dimension: str, value: float):
        """
        Mutate a specific dimensional gene

        Args:
            dimension: Dimension to mutate ('ontological', 'teleological', etc.)
            value: New gene value (0.0-1.0)
        """
        if dimension in self.genes:
            self.genes[dimension].append(value)
            self.last_update = datetime.utcnow().isoformat() + 'Z'

    def get_gene_trajectory(self, dimension: str) -> list[float]:
        """
        Get evolutionary trajectory of a dimensional gene

        Args:
            dimension: Dimension name

        Returns:
            List of gene values over time
        """
        return self.genes.get(dimension, [])

    def calculate_genetic_diversity(self) -> float:
        """
        Calculate genetic diversity (variance across dimensions)

        Returns:
            Diversity score (0.0-1.0)
        """
        if not any(self.genes.values()):
            return 0.0

        # Get latest value from each dimension
        latest_values = [genes[-1] for genes in self.genes.values() if genes]

        if not latest_values:
            return 0.0

        # Calculate variance
        mean = sum(latest_values) / len(latest_values)
        variance = sum((v - mean) ** 2 for v in latest_values) / len(latest_values)

        # Normalize to 0-1 range (variance can be at most 0.25 for values in [0,1])
        return min(1.0, variance / 0.25)

    def to_dict(self) -> dict:
        """Convert genome to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert genome to JSON string"""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> 'EntelechyGenome':
        """Create genome from dictionary"""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> 'EntelechyGenome':
        """Create genome from JSON string"""
        return cls.from_dict(json.loads(json_str))
