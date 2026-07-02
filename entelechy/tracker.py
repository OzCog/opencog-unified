"""
Entelechy Tracker

Evolutionary trajectory monitoring for tracking entelechy evolution over time.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .genome import EntelechyGenome
from .introspector import EntelechyIntrospector
from .types import EntelechyMetrics


@dataclass
class EntelechySnapshot:
    """Snapshot of entelechy state at a specific time"""

    timestamp: str
    metrics: dict
    fragmentations: int
    fitness: float
    development_stage: str
    genome_id: str


class EntelechyTracker:
    """
    Track entelechy evolution over time

    Monitors evolutionary trajectory, records snapshots,
    and analyzes long-term trends in actualization.
    """

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path).resolve()
        self.history: list[EntelechySnapshot] = []
        self.genomes: list[EntelechyGenome] = []
        self.history_file = self.repo_path / ".entelechy_history.json"

        # Load existing history if available
        self._load_history()

    def snapshot(self) -> EntelechySnapshot:
        """
        Take entelechy snapshot

        Returns:
            EntelechySnapshot with current state
        """
        # Perform introspection
        introspector = EntelechyIntrospector(str(self.repo_path))
        report = introspector.perform_deep_introspection()

        # Create genome from metrics
        metrics_dict = report["entelechy_assessment"]
        metrics = EntelechyMetrics(
            actualization_score=metrics_dict["actualization_score"],
            coherence_score=metrics_dict["coherence_score"],
            vitality_score=metrics_dict["vitality_score"],
            completeness_score=metrics_dict["completeness_score"],
            alignment_score=metrics_dict["alignment_score"],
        )

        parent_genome = self.genomes[-1] if self.genomes else None
        genome = EntelechyGenome.from_metrics(metrics, parent_genome)
        self.genomes.append(genome)

        # Create snapshot
        snapshot = EntelechySnapshot(
            timestamp=datetime.utcnow().isoformat() + "Z",
            metrics=metrics_dict,
            fragmentations=report["fragmentation_analysis"]["total_fragments"],
            fitness=metrics.fitness(),
            development_stage=metrics_dict["development_stage"],
            genome_id=genome.id,
        )

        self.history.append(snapshot)
        self._save_history()

        return snapshot

    def analyze_trajectory(self) -> dict:
        """
        Analyze evolutionary trajectory

        Returns:
            Dictionary with trajectory analysis
        """
        if len(self.history) < 2:
            return {"status": "insufficient_history", "message": "Need at least 2 snapshots for trajectory analysis"}

        first = self.history[0]
        last = self.history[-1]

        actualization_gain = last.metrics["actualization_score"] - first.metrics["actualization_score"]

        fragmentation_reduction = first.fragmentations - last.fragmentations
        fitness_gain = last.fitness - first.fitness

        # Determine trajectory
        if actualization_gain > 0.1:
            trajectory = "rapid_improvement"
        elif actualization_gain > 0:
            trajectory = "steady_improvement"
        elif actualization_gain > -0.05:
            trajectory = "stable"
        else:
            trajectory = "declining"

        # Calculate velocity (rate of change)
        time_delta = self._calculate_time_delta(first.timestamp, last.timestamp)
        velocity = actualization_gain / time_delta if time_delta > 0 else 0.0

        return {
            "status": "analyzed",
            "trajectory": trajectory,
            "actualization_gain": actualization_gain,
            "fragmentation_reduction": fragmentation_reduction,
            "fitness_gain": fitness_gain,
            "velocity": velocity,
            "total_snapshots": len(self.history),
            "time_span_days": time_delta,
            "first_snapshot": first.timestamp,
            "last_snapshot": last.timestamp,
        }

    def get_dimensional_evolution(self, dimension: str) -> list[float]:
        """
        Get evolution of a specific dimension over time

        Args:
            dimension: Dimension name (e.g., 'actualization_score')

        Returns:
            List of values over time
        """
        return [snapshot.metrics.get(dimension, 0.0) for snapshot in self.history]

    def predict_future_state(self, days_ahead: int = 30) -> dict:
        """
        Predict future entelechy state based on current trajectory

        Args:
            days_ahead: Number of days to predict ahead

        Returns:
            Predicted state dictionary
        """
        trajectory = self.analyze_trajectory()

        if trajectory["status"] != "analyzed":
            return {"status": "prediction_unavailable", "reason": trajectory["message"]}

        current = self.history[-1]
        velocity = trajectory["velocity"]

        # Simple linear prediction
        predicted_actualization = min(1.0, max(0.0, current.metrics["actualization_score"] + (velocity * days_ahead)))

        # Predict development stage
        if predicted_actualization < 0.3:
            predicted_stage = "embryonic"
        elif predicted_actualization < 0.6:
            predicted_stage = "juvenile"
        elif predicted_actualization < 0.8:
            predicted_stage = "mature"
        else:
            predicted_stage = "transcendent"

        return {
            "status": "predicted",
            "days_ahead": days_ahead,
            "current_actualization": current.metrics["actualization_score"],
            "predicted_actualization": predicted_actualization,
            "current_stage": current.development_stage,
            "predicted_stage": predicted_stage,
            "confidence": self._calculate_prediction_confidence(),
        }

    def _calculate_time_delta(self, time1: str, time2: str) -> float:
        """Calculate time delta in days between two timestamps"""
        try:
            t1 = datetime.fromisoformat(time1.replace("Z", "+00:00"))
            t2 = datetime.fromisoformat(time2.replace("Z", "+00:00"))
            return (t2 - t1).total_seconds() / 86400  # Convert to days
        except Exception:
            return 1.0  # Default to 1 day if parsing fails

    def _calculate_prediction_confidence(self) -> float:
        """Calculate confidence in predictions based on history length"""
        if len(self.history) < 5:
            return 0.3
        elif len(self.history) < 10:
            return 0.6
        elif len(self.history) < 20:
            return 0.8
        else:
            return 0.95

    def _load_history(self):
        """Load history from file"""
        if not self.history_file.exists():
            return

        try:
            with open(self.history_file) as f:
                data = json.load(f)

            # Reconstruct snapshots
            for snapshot_data in data.get("snapshots", []):
                self.history.append(EntelechySnapshot(**snapshot_data))

            # Reconstruct genomes
            for genome_data in data.get("genomes", []):
                self.genomes.append(EntelechyGenome.from_dict(genome_data))

        except Exception as e:
            print(f"Warning: Could not load history: {e}")

    def _save_history(self):
        """Save history to file"""
        data = {
            "snapshots": [
                {
                    "timestamp": s.timestamp,
                    "metrics": s.metrics,
                    "fragmentations": s.fragmentations,
                    "fitness": s.fitness,
                    "development_stage": s.development_stage,
                    "genome_id": s.genome_id,
                }
                for s in self.history
            ],
            "genomes": [g.to_dict() for g in self.genomes],
        }

        try:
            with open(self.history_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save history: {e}")

    def export_history(self, output_path: str):
        """Export history to JSON file"""
        trajectory = self.analyze_trajectory()

        export_data = {
            "tracker_info": {
                "repo_path": str(self.repo_path),
                "total_snapshots": len(self.history),
                "total_genomes": len(self.genomes),
            },
            "trajectory_analysis": trajectory,
            "snapshots": [
                {
                    "timestamp": s.timestamp,
                    "metrics": s.metrics,
                    "fragmentations": s.fragmentations,
                    "fitness": s.fitness,
                    "development_stage": s.development_stage,
                    "genome_id": s.genome_id,
                }
                for s in self.history
            ],
        }

        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2)
