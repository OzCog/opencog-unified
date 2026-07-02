"""
Entelechy Resonance

Detection and analysis of dimensional resonance - when multiple dimensions
achieve high scores simultaneously, creating emergent coherence.
"""

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from .types import EntelechyMetrics


def detect_resonance(metrics: EntelechyMetrics, threshold: float = 0.7) -> dict:
    """
    Detect resonance - multiple dimensions in harmony

    Args:
        metrics: Entelechy metrics to analyze
        threshold: Minimum score for resonance detection (default: 0.7)

    Returns:
        Dictionary with resonance analysis
    """
    dimensions = [
        metrics.actualization_score,
        metrics.completeness_score,
        metrics.coherence_score,
        metrics.vitality_score,
        metrics.alignment_score,
    ]

    # Check if all dimensions above threshold
    above_threshold = all(d > threshold for d in dimensions)

    # Calculate statistics
    if HAS_NUMPY:
        mean_level = float(np.mean(dimensions))
        variance = float(np.var(dimensions))
        std_dev = float(np.std(dimensions))
    else:
        mean_level = sum(dimensions) / len(dimensions)
        variance = sum((d - mean_level) ** 2 for d in dimensions) / len(dimensions)
        std_dev = variance**0.5

    # Determine resonance quality
    if variance < 0.01:
        quality = "high"
        resonating = True
    elif variance < 0.05:
        quality = "moderate"
        resonating = above_threshold
    else:
        quality = "low"
        resonating = False

    # Identify strongest and weakest dimensions
    dimension_names = ["actualization", "completeness", "coherence", "vitality", "alignment"]
    dimension_scores = dict(zip(dimension_names, dimensions, strict=False))
    strongest = max(dimension_scores, key=dimension_scores.get)
    weakest = min(dimension_scores, key=dimension_scores.get)

    # Calculate resonance strength (0.0-1.0)
    resonance_strength = mean_level * (1.0 - min(1.0, variance / 0.05))

    return {
        "resonating": resonating,
        "quality": quality,
        "mean_level": mean_level,
        "variance": variance,
        "std_dev": std_dev,
        "resonance_strength": resonance_strength,
        "threshold": threshold,
        "dimensions_above_threshold": sum(1 for d in dimensions if d > threshold),
        "total_dimensions": len(dimensions),
        "strongest_dimension": strongest,
        "weakest_dimension": weakest,
        "dimension_scores": dimension_scores,
    }


def detect_resonance_cascade(metrics_history: list[EntelechyMetrics]) -> dict:
    """
    Detect resonance cascade - improvement in one dimension triggering others

    Args:
        metrics_history: List of metrics over time

    Returns:
        Dictionary with cascade analysis
    """
    if len(metrics_history) < 2:
        return {"status": "insufficient_data", "message": "Need at least 2 metric snapshots for cascade detection"}

    cascades = []

    for i in range(1, len(metrics_history)):
        prev = metrics_history[i - 1]
        curr = metrics_history[i]

        # Calculate improvements
        improvements = {
            "actualization": curr.actualization_score - prev.actualization_score,
            "completeness": curr.completeness_score - prev.completeness_score,
            "coherence": curr.coherence_score - prev.coherence_score,
            "vitality": curr.vitality_score - prev.vitality_score,
            "alignment": curr.alignment_score - prev.alignment_score,
        }

        # Identify significant improvements (> 0.1)
        significant = {k: v for k, v in improvements.items() if v > 0.1}

        if len(significant) >= 2:
            # Multiple dimensions improved - potential cascade
            cascades.append(
                {
                    "index": i,
                    "trigger_dimension": max(significant, key=significant.get),
                    "affected_dimensions": list(significant.keys()),
                    "improvements": significant,
                }
            )

    return {
        "status": "analyzed",
        "total_snapshots": len(metrics_history),
        "cascades_detected": len(cascades),
        "cascades": cascades,
        "has_cascading": len(cascades) > 0,
    }


def calculate_dimensional_balance(metrics: EntelechyMetrics) -> dict:
    """
    Calculate dimensional balance using weighted RMS

    Health(system) = √(Σᵢ wᵢ · Dᵢ²) / Σᵢ wᵢ

    Args:
        metrics: Entelechy metrics

    Returns:
        Dictionary with balance analysis
    """
    # Weights for each dimension
    weights = {
        "ontological": 0.2,  # Completeness
        "teleological": 0.25,  # Alignment
        "cognitive": 0.25,  # Actualization
        "integrative": 0.15,  # Coherence
        "evolutionary": 0.15,  # Vitality
    }

    dimensions = {
        "ontological": metrics.completeness_score,
        "teleological": metrics.alignment_score,
        "cognitive": metrics.actualization_score,
        "integrative": metrics.coherence_score,
        "evolutionary": metrics.vitality_score,
    }

    # Calculate weighted RMS
    weighted_sum_squares = sum(weights[k] * (dimensions[k] ** 2) for k in weights)
    sum_weights = sum(weights.values())

    if HAS_NUMPY:
        health = float(np.sqrt(weighted_sum_squares / sum_weights))
        values = list(dimensions.values())
        mean = float(np.mean(values))
        imbalance = float(np.var(values))
    else:
        health = (weighted_sum_squares / sum_weights) ** 0.5
        values = list(dimensions.values())
        mean = sum(values) / len(values)
        imbalance = sum((v - mean) ** 2 for v in values) / len(values)

    return {
        "health": float(health),
        "imbalance": float(imbalance),
        "dimensions": dimensions,
        "weights": weights,
        "balanced": imbalance < 0.05,
    }
