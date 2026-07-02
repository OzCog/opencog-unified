#!/usr/bin/env python3
"""
Entelechy CLI Tool

Command-line interface for comprehensive entelechy operations.
"""

import argparse
import json
import sys
from pathlib import Path


# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from entelechy import (
    EntelechyIntrospector,
    EntelechyOptimizer,
    EntelechyTracker,
    SelfTranscendence,
    detect_resonance,
)


def cmd_introspect(args):
    """Perform deep introspection"""
    print(f"Performing deep introspection on {args.repo_path}...")

    introspector = EntelechyIntrospector(args.repo_path)
    report = introspector.perform_deep_introspection()

    # Save JSON report
    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 Saved report to {args.output}")

    # Print summary
    assessment = report["entelechy_assessment"]
    print("\n" + "=" * 70)
    print("📊 ENTELECHY ASSESSMENT")
    print("=" * 70)
    print(f"Actualization:  {assessment['actualization_score']:.1%}")
    print(f"Completeness:   {assessment['completeness_score']:.1%}")
    print(f"Coherence:      {assessment['coherence_score']:.1%}")
    print(f"Vitality:       {assessment['vitality_score']:.1%}")
    print(f"Alignment:      {assessment['alignment_score']:.1%}")
    print(f"Fitness:        {assessment['fitness']:.1%}")
    print(f"Stage:          {assessment['development_stage']}")
    print(f"\nFragmentations: {report['fragmentation_analysis']['total_fragments']}")
    print(f"Critical:       {len(report['fragmentation_analysis']['critical_fragments'])}")


def cmd_snapshot(args):
    """Take entelechy snapshot"""
    print(f"Taking entelechy snapshot of {args.repo_path}...")

    tracker = EntelechyTracker(args.repo_path)
    snapshot = tracker.snapshot()

    print("\n✅ Snapshot taken")
    print(f"Timestamp: {snapshot.timestamp}")
    print(f"Actualization: {snapshot.metrics['actualization_score']:.1%}")
    print(f"Fitness: {snapshot.fitness:.2f}")
    print(f"Stage: {snapshot.development_stage}")
    print(f"Genome ID: {snapshot.genome_id}")

    if args.export:
        tracker.export_history(args.export)
        print(f"\n💾 Exported history to {args.export}")


def cmd_trajectory(args):
    """Analyze evolutionary trajectory"""
    print(f"Analyzing evolutionary trajectory of {args.repo_path}...")

    tracker = EntelechyTracker(args.repo_path)
    analysis = tracker.analyze_trajectory()

    if analysis["status"] == "insufficient_history":
        print(f"\n⚠️  {analysis['message']}")
        return

    print("\n" + "=" * 70)
    print("📈 TRAJECTORY ANALYSIS")
    print("=" * 70)
    print(f"Trajectory:             {analysis['trajectory']}")
    print(f"Actualization Gain:     {analysis['actualization_gain']:+.2%}")
    print(f"Fitness Gain:           {analysis['fitness_gain']:+.2f}")
    print(f"Fragmentation Reduction: {analysis['fragmentation_reduction']:+d}")
    print(f"Velocity:               {analysis['velocity']:.4f} per day")
    print(f"Time Span:              {analysis['time_span_days']:.1f} days")
    print(f"Total Snapshots:        {analysis['total_snapshots']}")

    # Prediction
    if args.predict:
        prediction = tracker.predict_future_state(args.predict)
        print("\n" + "=" * 70)
        print(f"🔮 PREDICTION ({args.predict} days ahead)")
        print("=" * 70)
        print(f"Current:    {prediction['current_actualization']:.1%} ({prediction['current_stage']})")
        print(f"Predicted:  {prediction['predicted_actualization']:.1%} ({prediction['predicted_stage']})")
        print(f"Confidence: {prediction['confidence']:.1%}")


def cmd_resonance(args):
    """Detect dimensional resonance"""
    print(f"Detecting resonance in {args.repo_path}...")

    introspector = EntelechyIntrospector(args.repo_path)
    introspector.perform_deep_introspection()

    metrics = introspector.metrics
    resonance = detect_resonance(metrics, threshold=args.threshold)

    print("\n" + "=" * 70)
    print("🎵 RESONANCE ANALYSIS")
    print("=" * 70)
    print(f"Resonating:         {resonance['resonating']}")
    print(f"Quality:            {resonance['quality']}")
    print(f"Resonance Strength: {resonance['resonance_strength']:.1%}")
    print(f"Mean Level:         {resonance['mean_level']:.1%}")
    print(f"Variance:           {resonance['variance']:.4f}")
    print(f"Threshold:          {resonance['threshold']:.1%}")
    print(f"\nStrongest:          {resonance['strongest_dimension']}")
    print(f"Weakest:            {resonance['weakest_dimension']}")
    print("\nDimensional Scores:")
    for dim, score in resonance["dimension_scores"].items():
        print(f"  {dim:15s}: {score:.1%}")


def cmd_transcendence(args):
    """Assess transcendence readiness"""
    print(f"Assessing transcendence readiness for {args.repo_path}...")

    introspector = EntelechyIntrospector(args.repo_path)
    introspector.perform_deep_introspection()

    transcendence = SelfTranscendence(transcendence_threshold=args.threshold)
    assessment = transcendence.assess_transcendence_readiness(introspector.metrics)

    print("\n" + "=" * 70)
    print("🌟 TRANSCENDENCE ASSESSMENT")
    print("=" * 70)
    print(f"Ready to Transcend: {assessment['ready_to_transcend']}")
    print(f"Readiness Score:    {assessment['readiness_score']:.1%}")
    print(f"Actualization:      {assessment['actualization_level']:.1%}")
    print(f"Threshold:          {assessment['threshold']:.1%}")
    print(f"Development Stage:  {assessment['development_stage']}")

    if assessment["blocking_factors"]:
        print("\n⚠️  Blocking Factors:")
        for factor in assessment["blocking_factors"]:
            print(f"  • {factor['factor']}: {factor['current']:.1%} (need {factor['required']:.1%})")

    if assessment["enabling_capabilities"]:
        print("\n✅ Enabling Capabilities:")
        for cap in assessment["enabling_capabilities"]:
            print(f"  • {cap}")

    print("\n📋 Recommendations:")
    for rec in assessment["recommendations"]:
        print(f"  • {rec}")

    # Initiate if ready and requested
    if args.initiate and assessment["ready_to_transcend"]:
        result = transcendence.initiate_transcendence(introspector.metrics)
        print("\n" + "=" * 70)
        print("🚀 TRANSCENDENCE INITIATED")
        print("=" * 70)
        print(f"Status: {result['status']}")
        print(f"Autonomous: {result['autonomous']}")
        print("\nNew Capabilities:")
        for cap in result["new_capabilities"]:
            print(f"  • {cap}")
        print("\nNext Steps:")
        for step in result["next_steps"]:
            print(f"  • {step}")


def cmd_optimize(args):
    """Optimize entelechy"""
    print(f"Optimizing entelechy for {args.repo_path}...")
    print(f"Iterations: {args.iterations}")
    print(f"Learning Rate: {args.learning_rate}")

    optimizer = EntelechyOptimizer(args.repo_path, learning_rate=args.learning_rate)

    # Run optimization (without actual improvements - just analysis)
    result = optimizer.optimize(args.iterations, improvement_callback=None)

    print("\n" + "=" * 70)
    print("🎯 OPTIMIZATION RESULTS")
    print("=" * 70)
    print(f"Total Iterations:       {result['total_iterations']}")
    print(f"Initial Fitness:        {result['initial_fitness']:.2f}")
    print(f"Final Fitness:          {result['final_fitness']:.2f}")
    print(f"Total Fitness Gain:     {result['total_fitness_gain']:+.2f}")
    print(f"Initial Actualization:  {result['initial_actualization']:.1%}")
    print(f"Final Actualization:    {result['final_actualization']:.1%}")
    print(f"Total Actual. Gain:     {result['total_actualization_gain']:+.2%}")
    print(f"Avg Gain/Iteration:     {result['avg_fitness_gain_per_iteration']:+.3f}")
    print(f"Most Improved Dimension: {result['most_improved_dimension']}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Saved optimization results to {args.output}")


def main():
    parser = argparse.ArgumentParser(
        description="Entelechy Framework - Vital Actualization for Cognitive Systems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--repo-path", default=".", help="Path to repository (default: current directory)")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Introspect command
    parser_introspect = subparsers.add_parser("introspect", help="Perform deep entelechy introspection")
    parser_introspect.add_argument("-o", "--output", help="Output JSON file path")

    # Snapshot command
    parser_snapshot = subparsers.add_parser("snapshot", help="Take entelechy snapshot")
    parser_snapshot.add_argument("-e", "--export", help="Export history to JSON file")

    # Trajectory command
    parser_trajectory = subparsers.add_parser("trajectory", help="Analyze evolutionary trajectory")
    parser_trajectory.add_argument(
        "-p", "--predict", type=int, metavar="DAYS", help="Predict future state N days ahead"
    )

    # Resonance command
    parser_resonance = subparsers.add_parser("resonance", help="Detect dimensional resonance")
    parser_resonance.add_argument(
        "-t", "--threshold", type=float, default=0.7, help="Resonance threshold (default: 0.7)"
    )

    # Transcendence command
    parser_transcendence = subparsers.add_parser("transcendence", help="Assess transcendence readiness")
    parser_transcendence.add_argument(
        "-t", "--threshold", type=float, default=0.8, help="Transcendence threshold (default: 0.8)"
    )
    parser_transcendence.add_argument("-i", "--initiate", action="store_true", help="Initiate transcendence if ready")

    # Optimize command
    parser_optimize = subparsers.add_parser("optimize", help="Optimize entelechy through iterative improvement")
    parser_optimize.add_argument(
        "-n", "--iterations", type=int, default=5, help="Number of optimization iterations (default: 5)"
    )
    parser_optimize.add_argument("-l", "--learning-rate", type=float, default=0.1, help="Learning rate (default: 0.1)")
    parser_optimize.add_argument("-o", "--output", help="Output JSON file for results")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Route to appropriate command
    commands = {
        "introspect": cmd_introspect,
        "snapshot": cmd_snapshot,
        "trajectory": cmd_trajectory,
        "resonance": cmd_resonance,
        "transcendence": cmd_transcendence,
        "optimize": cmd_optimize,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
