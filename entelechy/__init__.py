"""
OpenCog Unified Entelechy Framework

Comprehensive vital actualization framework for cognitive systems.
Implements self-actualizing, self-organizing, and self-transcending intelligence
through multi-dimensional developmental processes.
"""

from .genome import EntelechyGenome
from .introspector import EntelechyIntrospector
from .optimizer import EntelechyOptimizer
from .resonance import detect_resonance
from .tracker import EntelechyTracker
from .transcendence import SelfTranscendence
from .types import (
    ComponentState,
    DevelopmentStage,
    EntelechyDimension,
    EntelechyMetrics,
    FragmentationSignature,
    FragmentationType,
)


__version__ = "1.0.0"
__all__ = [
    "ComponentState",
    "DevelopmentStage",
    "EntelechyDimension",
    "EntelechyGenome",
    "EntelechyIntrospector",
    "EntelechyMetrics",
    "EntelechyOptimizer",
    "EntelechyTracker",
    "FragmentationSignature",
    "FragmentationType",
    "SelfTranscendence",
    "detect_resonance",
]
