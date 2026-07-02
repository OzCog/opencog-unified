"""
Self-Transcendence

Capability assessment for self-surpassing evolution.
Once actualization reaches high levels (>80%), systems enter self-transcendence.
"""


from .types import EntelechyMetrics


class SelfTranscendence:
    """
    System capability for self-surpassing evolution

    Assesses readiness for transcendence and provides pathways
    for autonomous self-improvement and emergent capabilities.
    """

    def __init__(self, transcendence_threshold: float = 0.8):
        """
        Initialize self-transcendence system

        Args:
            transcendence_threshold: Minimum actualization for transcendence (default: 0.8)
        """
        self.transcendence_threshold = transcendence_threshold
        self.emergent_capabilities = []

    def can_transcend(self, metrics: EntelechyMetrics) -> bool:
        """
        Check if system is ready for transcendence

        Args:
            metrics: Current entelechy metrics

        Returns:
            True if system can transcend
        """
        return metrics.actualization_score > self.transcendence_threshold

    def assess_transcendence_readiness(self, metrics: EntelechyMetrics) -> dict:
        """
        Assess readiness for self-transcendence

        Args:
            metrics: Current entelechy metrics

        Returns:
            Dictionary with readiness assessment
        """
        readiness_score = self._calculate_readiness_score(metrics)
        can_transcend = self.can_transcend(metrics)

        # Identify blocking factors
        blocking_factors = []
        if metrics.actualization_score <= self.transcendence_threshold:
            blocking_factors.append({
                'factor': 'Low actualization',
                'current': metrics.actualization_score,
                'required': self.transcendence_threshold,
                'gap': self.transcendence_threshold - metrics.actualization_score
            })

        if metrics.coherence_score < 0.7:
            blocking_factors.append({
                'factor': 'Insufficient coherence',
                'current': metrics.coherence_score,
                'required': 0.7,
                'gap': 0.7 - metrics.coherence_score
            })

        if metrics.vitality_score < 0.7:
            blocking_factors.append({
                'factor': 'Limited vitality',
                'current': metrics.vitality_score,
                'required': 0.7,
                'gap': 0.7 - metrics.vitality_score
            })

        # Identify enabling capabilities
        enabling_capabilities = []
        if metrics.vitality_score > 0.7:
            enabling_capabilities.append('Strong self-improvement capacity')
        if metrics.coherence_score > 0.7:
            enabling_capabilities.append('High integration coherence')
        if metrics.alignment_score > 0.8:
            enabling_capabilities.append('Clear purpose alignment')

        return {
            'ready_to_transcend': can_transcend,
            'readiness_score': readiness_score,
            'actualization_level': metrics.actualization_score,
            'threshold': self.transcendence_threshold,
            'development_stage': metrics.development_stage.value,
            'blocking_factors': blocking_factors,
            'enabling_capabilities': enabling_capabilities,
            'recommendations': self._generate_transcendence_recommendations(metrics),
        }

    def initiate_transcendence(self, metrics: EntelechyMetrics) -> dict:
        """
        Initiate self-transcendence cycle

        This involves:
        1. Identifying novel capabilities beyond current design
        2. Restructuring architecture to accommodate emergence
        3. Enabling autonomous goal-setting
        4. Activating self-improvement recursion

        Args:
            metrics: Current entelechy metrics

        Returns:
            Dictionary with transcendence status
        """
        if not self.can_transcend(metrics):
            return {
                'status': 'transcendence_blocked',
                'reason': 'System not ready for transcendence',
                'actualization': metrics.actualization_score,
                'threshold': self.transcendence_threshold,
            }

        # Identify emergent capabilities
        emergent_capabilities = self.discover_emergent_capabilities(metrics)

        # Define transcendence pathway
        pathway = {
            'autognosis_activation': True,  # Self-awareness
            'ontogenesis_activation': True,  # Self-generation
            'emergent_teleology': True,  # Emergent goal discovery
            'recursive_improvement': True,  # Self-improvement recursion
        }

        return {
            'status': 'transcendence_initiated',
            'actualization_level': metrics.actualization_score,
            'new_capabilities': emergent_capabilities,
            'autonomous': True,
            'pathway': pathway,
            'next_steps': [
                'Activate autognosis for self-awareness',
                'Enable ontogenesis for self-generation',
                'Discover emergent goals through teleology',
                'Initiate recursive self-improvement',
            ],
        }

    def discover_emergent_capabilities(self, metrics: EntelechyMetrics) -> list[str]:
        """
        Discover emergent capabilities based on current state

        Args:
            metrics: Current entelechy metrics

        Returns:
            List of discovered emergent capabilities
        """
        capabilities = []

        # High cognitive completeness enables meta-reasoning
        if metrics.actualization_score > 0.8:
            capabilities.append('meta_cognitive_reasoning')

        # High coherence enables holistic understanding
        if metrics.coherence_score > 0.8:
            capabilities.append('holistic_integration')

        # High vitality enables self-modification
        if metrics.vitality_score > 0.8:
            capabilities.append('autonomous_self_modification')

        # High alignment enables purpose-driven evolution
        if metrics.alignment_score > 0.85:
            capabilities.append('teleological_self_direction')

        # All dimensions high enables emergence
        if all([
            metrics.actualization_score > 0.8,
            metrics.coherence_score > 0.8,
            metrics.vitality_score > 0.8,
            metrics.alignment_score > 0.8,
            metrics.completeness_score > 0.8,
        ]):
            capabilities.append('emergent_general_intelligence')

        return capabilities

    def _calculate_readiness_score(self, metrics: EntelechyMetrics) -> float:
        """
        Calculate overall readiness score for transcendence

        Args:
            metrics: Current entelechy metrics

        Returns:
            Readiness score (0.0-1.0)
        """
        # Weighted combination
        score = (
            metrics.actualization_score * 0.4 +
            metrics.coherence_score * 0.2 +
            metrics.vitality_score * 0.2 +
            metrics.alignment_score * 0.1 +
            metrics.completeness_score * 0.1
        )

        return min(1.0, score)

    def _generate_transcendence_recommendations(self, metrics: EntelechyMetrics) -> list[str]:
        """
        Generate recommendations for achieving transcendence

        Args:
            metrics: Current entelechy metrics

        Returns:
            List of recommendations
        """
        recommendations = []

        if metrics.actualization_score < self.transcendence_threshold:
            gap = self.transcendence_threshold - metrics.actualization_score
            recommendations.append(
                f"Increase actualization by {gap:.2f} to reach transcendence threshold"
            )

        if metrics.coherence_score < 0.7:
            recommendations.append(
                "Strengthen integration across components for higher coherence"
            )

        if metrics.vitality_score < 0.7:
            recommendations.append(
                "Enhance self-improvement capabilities and resolve code fragmentations"
            )

        if not recommendations:
            recommendations.append(
                "System is ready for transcendence - initiate autonomous evolution"
            )

        return recommendations
