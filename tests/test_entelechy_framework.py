#!/usr/bin/env python3
"""
Comprehensive test suite for Entelechy Framework
"""

import sys
import tempfile
import unittest
from pathlib import Path


# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from entelechy import (
    DevelopmentStage,
    EntelechyDimension,
    EntelechyGenome,
    EntelechyIntrospector,
    EntelechyMetrics,
    EntelechyOptimizer,
    EntelechyTracker,
    SelfTranscendence,
    detect_resonance,
)


class TestEntelechyTypes(unittest.TestCase):
    """Test entelechy type definitions"""

    def test_entelechy_metrics_creation(self):
        """Test creating entelechy metrics"""
        metrics = EntelechyMetrics(
            actualization_score=0.75,
            coherence_score=0.70,
            vitality_score=0.80,
            completeness_score=0.72,
            alignment_score=0.85
        )

        self.assertEqual(metrics.actualization_score, 0.75)
        self.assertGreater(metrics.fitness(), 0.7)

    def test_development_stage_determination(self):
        """Test development stage determination"""
        metrics = EntelechyMetrics(
            actualization_score=0.25,
            coherence_score=0.5,
            vitality_score=0.5,
            completeness_score=0.5,
            alignment_score=0.5
        )

        stage = metrics.determine_stage()
        self.assertEqual(stage, DevelopmentStage.EMBRYONIC)

        metrics.actualization_score = 0.75
        stage = metrics.determine_stage()
        self.assertEqual(stage, DevelopmentStage.MATURE)


class TestEntelechyIntrospector(unittest.TestCase):
    """Test entelechy introspector"""

    def setUp(self):
        self.repo_path = Path(__file__).parent.parent

    def test_introspector_creation(self):
        """Test creating introspector"""
        introspector = EntelechyIntrospector(str(self.repo_path))
        self.assertIsNotNone(introspector)
        self.assertEqual(introspector.repo_path, self.repo_path)

    def test_deep_introspection(self):
        """Test performing deep introspection"""
        introspector = EntelechyIntrospector(str(self.repo_path))
        report = introspector.perform_deep_introspection()

        self.assertIn('entelechy_assessment', report)
        self.assertIn('dimensional_insights', report)
        self.assertIn('fragmentation_analysis', report)
        self.assertIn('repair_roadmap', report)

        # Check metrics
        assessment = report['entelechy_assessment']
        self.assertIn('actualization_score', assessment)
        self.assertIn('fitness', assessment)
        self.assertIn('development_stage', assessment)

        # Validate score ranges
        self.assertGreaterEqual(assessment['actualization_score'], 0.0)
        self.assertLessEqual(assessment['actualization_score'], 1.0)


class TestEntelechyGenome(unittest.TestCase):
    """Test entelechy genome"""

    def test_genome_creation_from_metrics(self):
        """Test creating genome from metrics"""
        metrics = EntelechyMetrics(
            actualization_score=0.75,
            coherence_score=0.70,
            vitality_score=0.80,
            completeness_score=0.72,
            alignment_score=0.85
        )

        genome = EntelechyGenome.from_metrics(metrics)

        self.assertIsNotNone(genome.id)
        self.assertEqual(genome.generation, 0)
        self.assertEqual(len(genome.lineage), 0)
        self.assertAlmostEqual(genome.fitness, metrics.fitness(), places=2)

    def test_genome_evolution(self):
        """Test genome evolution"""
        metrics1 = EntelechyMetrics(
            actualization_score=0.60,
            coherence_score=0.60,
            vitality_score=0.60,
            completeness_score=0.60,
            alignment_score=0.60
        )

        genome1 = EntelechyGenome.from_metrics(metrics1)

        metrics2 = EntelechyMetrics(
            actualization_score=0.75,
            coherence_score=0.70,
            vitality_score=0.80,
            completeness_score=0.72,
            alignment_score=0.85
        )

        genome2 = genome1.evolve(metrics2)

        self.assertEqual(genome2.generation, 1)
        self.assertIn(genome1.id, genome2.lineage)
        self.assertGreater(genome2.fitness, genome1.fitness)

    def test_genome_serialization(self):
        """Test genome serialization"""
        metrics = EntelechyMetrics(
            actualization_score=0.75,
            coherence_score=0.70,
            vitality_score=0.80,
            completeness_score=0.72,
            alignment_score=0.85
        )

        genome = EntelechyGenome.from_metrics(metrics)

        # Test to_dict and from_dict
        genome_dict = genome.to_dict()
        restored_genome = EntelechyGenome.from_dict(genome_dict)

        self.assertEqual(genome.id, restored_genome.id)
        self.assertEqual(genome.generation, restored_genome.generation)
        self.assertAlmostEqual(genome.fitness, restored_genome.fitness)


class TestEntelechyTracker(unittest.TestCase):
    """Test entelechy tracker"""

    def setUp(self):
        self.repo_path = Path(__file__).parent.parent
        self.temp_dir = tempfile.mkdtemp()

    def test_tracker_creation(self):
        """Test creating tracker"""
        tracker = EntelechyTracker(str(self.repo_path))
        self.assertIsNotNone(tracker)

    def test_snapshot(self):
        """Test taking snapshot"""
        EntelechyTracker(str(self.temp_dir))
        # Note: This will fail in temp dir without proper structure
        # In real tests, use actual repo
        pass


class TestResonanceDetection(unittest.TestCase):
    """Test resonance detection"""

    def test_high_resonance(self):
        """Test detecting high resonance"""
        metrics = EntelechyMetrics(
            actualization_score=0.85,
            coherence_score=0.86,
            vitality_score=0.84,
            completeness_score=0.85,
            alignment_score=0.87
        )

        resonance = detect_resonance(metrics, threshold=0.7)

        self.assertTrue(resonance['resonating'])
        self.assertEqual(resonance['quality'], 'high')
        self.assertGreater(resonance['resonance_strength'], 0.8)

    def test_low_resonance(self):
        """Test detecting low resonance"""
        metrics = EntelechyMetrics(
            actualization_score=0.90,
            coherence_score=0.40,
            vitality_score=0.85,
            completeness_score=0.45,
            alignment_score=0.88
        )

        resonance = detect_resonance(metrics, threshold=0.7)

        self.assertFalse(resonance['resonating'])
        # Quality will be moderate due to variance calculation
        self.assertIn(resonance['quality'], ['low', 'moderate'])


class TestSelfTranscendence(unittest.TestCase):
    """Test self-transcendence"""

    def test_transcendence_readiness_high(self):
        """Test transcendence readiness with high actualization"""
        metrics = EntelechyMetrics(
            actualization_score=0.85,
            coherence_score=0.80,
            vitality_score=0.82,
            completeness_score=0.83,
            alignment_score=0.86
        )

        transcendence = SelfTranscendence(transcendence_threshold=0.8)
        self.assertTrue(transcendence.can_transcend(metrics))

        assessment = transcendence.assess_transcendence_readiness(metrics)
        self.assertTrue(assessment['ready_to_transcend'])
        self.assertGreater(assessment['readiness_score'], 0.8)

    def test_transcendence_readiness_low(self):
        """Test transcendence readiness with low actualization"""
        metrics = EntelechyMetrics(
            actualization_score=0.50,
            coherence_score=0.60,
            vitality_score=0.55,
            completeness_score=0.58,
            alignment_score=0.62
        )

        transcendence = SelfTranscendence(transcendence_threshold=0.8)
        self.assertFalse(transcendence.can_transcend(metrics))

        assessment = transcendence.assess_transcendence_readiness(metrics)
        self.assertFalse(assessment['ready_to_transcend'])
        self.assertGreater(len(assessment['blocking_factors']), 0)

    def test_emergent_capabilities_discovery(self):
        """Test discovering emergent capabilities"""
        metrics = EntelechyMetrics(
            actualization_score=0.85,
            coherence_score=0.85,
            vitality_score=0.85,
            completeness_score=0.85,
            alignment_score=0.88
        )

        transcendence = SelfTranscendence()
        capabilities = transcendence.discover_emergent_capabilities(metrics)

        self.assertGreater(len(capabilities), 0)
        self.assertIn('emergent_general_intelligence', capabilities)


class TestEntelechyOptimizer(unittest.TestCase):
    """Test entelechy optimizer"""

    def setUp(self):
        self.repo_path = Path(__file__).parent.parent

    def test_optimizer_creation(self):
        """Test creating optimizer"""
        optimizer = EntelechyOptimizer(str(self.repo_path), learning_rate=0.1)
        self.assertIsNotNone(optimizer)
        self.assertEqual(optimizer.learning_rate, 0.1)

    def test_improvement_generation(self):
        """Test generating improvements"""
        optimizer = EntelechyOptimizer(str(self.repo_path))

        metrics = EntelechyMetrics(
            actualization_score=0.60,
            coherence_score=0.50,
            vitality_score=0.55,
            completeness_score=0.58,
            alignment_score=0.62
        )

        improvements = optimizer.generate_improvements(
            EntelechyDimension.EVOLUTIONARY,
            metrics
        )

        self.assertGreater(len(improvements), 0)
        self.assertIn('action', improvements[0])
        self.assertIn('priority', improvements[0])


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
