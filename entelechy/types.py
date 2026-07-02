"""
Entelechy Framework Types

Core type definitions for the entelechy framework.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EntelechyDimension(Enum):
    """Dimensions of entelechy analysis"""
    ONTOLOGICAL = "ontological"  # Being - what the system IS
    TELEOLOGICAL = "teleological"  # Purpose - what the system is BECOMING
    COGNITIVE = "cognitive"  # Cognition - how the system THINKS
    INTEGRATIVE = "integrative"  # Integration - how parts UNITE
    EVOLUTIONARY = "evolutionary"  # Evolution - how the system GROWS


class FragmentationType(Enum):
    """Types of fragmentation identified"""
    INCOMPLETE_IMPLEMENTATION = "incomplete_implementation"
    MISSING_DEPENDENCY = "missing_dependency"
    COGNITIVE_DISCONNECT = "cognitive_disconnect"
    INTEGRATION_GAP = "integration_gap"
    EVOLUTIONARY_STAGNATION = "evolutionary_stagnation"
    PLACEHOLDER_CODE = "placeholder_code"
    BROKEN_LINKAGE = "broken_linkage"
    CONCEPTUAL_INCOHERENCE = "conceptual_incoherence"


class DevelopmentStage(Enum):
    """Development stages of cognitive system"""
    EMBRYONIC = "embryonic"  # Potentiality (< 30%)
    JUVENILE = "juvenile"  # Development (30-60%)
    MATURE = "mature"  # Actualization (60-80%)
    TRANSCENDENT = "transcendent"  # Self-Surpassing (> 80%)


@dataclass
class ComponentState:
    """State of a system component"""
    name: str
    exists: bool
    health: float  # 0.0-1.0
    dependencies_satisfied: bool = True
    fragmentation_count: int = 0
    implementation_depth: float = 1.0  # 0.0-1.0


@dataclass
class FragmentationSignature:
    """Signature of a fragmented aspect"""
    dimension: EntelechyDimension
    fragmentation_type: FragmentationType
    location: str
    severity: float  # 0.0-1.0, where 1.0 is critical
    description: str
    context: dict[str, Any] = field(default_factory=dict)
    repair_priority: int = 0
    repair_suggestions: list[str] = field(default_factory=list)


@dataclass
class EntelechyMetrics:
    """Quantitative metrics of system entelechy"""
    actualization_score: float  # 0.0-1.0, degree of potential realization
    coherence_score: float  # 0.0-1.0, holistic integration
    vitality_score: float  # 0.0-1.0, self-organizing capacity
    completeness_score: float  # 0.0-1.0, implementation completeness
    alignment_score: float  # 0.0-1.0, teleological alignment

    # Component metrics
    total_components: int = 0
    integrated_components: int = 0
    fragmented_components: int = 0

    # Code health metrics
    total_code_markers: int = 0
    todo_count: int = 0
    fixme_count: int = 0
    stub_count: int = 0

    # Cognitive architecture metrics
    cognitive_layers_complete: int = 0
    cognitive_layers_total: int = 0

    # Integration metrics
    dependency_satisfaction: float = 0.0
    cmake_integration_health: float = 0.0
    test_coverage_health: float = 0.0

    # Development stage
    development_stage: DevelopmentStage = DevelopmentStage.EMBRYONIC

    def fitness(self) -> float:
        """
        Calculate overall fitness score

        Fitness is a weighted combination of dimensional scores:
        fitness = ontological*0.2 + teleological*0.25 + cognitive*0.25 +
                  integrative*0.15 + evolutionary*0.15
        """
        ontological = self.completeness_score
        teleological = self.alignment_score
        cognitive = self.actualization_score
        integrative = self.coherence_score
        evolutionary = self.vitality_score

        return (
            ontological * 0.2 +
            teleological * 0.25 +
            cognitive * 0.25 +
            integrative * 0.15 +
            evolutionary * 0.15
        )

    def determine_stage(self) -> DevelopmentStage:
        """Determine development stage based on actualization"""
        if self.actualization_score < 0.3:
            return DevelopmentStage.EMBRYONIC
        elif self.actualization_score < 0.6:
            return DevelopmentStage.JUVENILE
        elif self.actualization_score < 0.8:
            return DevelopmentStage.MATURE
        else:
            return DevelopmentStage.TRANSCENDENT
