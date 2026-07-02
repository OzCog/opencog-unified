#!/usr/bin/env python3
"""
Entelechy Repair Framework Demo

Quick demonstration of the repair framework capabilities.
Shows key features and sample outputs.
"""

import json
from datetime import datetime
from pathlib import Path


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_marker_analysis():
    """Demonstrate marker analysis results."""
    print_header("MARKER ANALYSIS")

    analysis_file = Path('entelechy_marker_analysis.json')
    if not analysis_file.exists():
        print("⚠ Run: python3 entelechy_marker_analyzer.py")
        return

    with open(analysis_file) as f:
        data = json.load(f)

    print(f"\n📊 Total Markers Found: {data['summary']['total_markers']}")

    # Count by type
    markers = data.get('markers', [])
    by_type = {}
    for m in markers:
        mt = m.get('marker_type', 'unknown')
        by_type[mt] = by_type.get(mt, 0) + 1

    print("\n📋 By Type:")
    for marker_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(markers) * 100) if markers else 0
        print(f"   {marker_type:20s} {count:4d} ({pct:5.1f}%)")

    # Show sample markers
    print("\n🔍 Sample Markers (first 5):")
    for i, marker in enumerate(markers[:5], 1):
        print(f"\n   {i}. [{marker['marker_type']}] {marker['file_path']}:{marker['line_number']}")
        print(f"      Category: {marker['category']}")
        print(f"      Severity: {marker['severity']:.2f}")
        content = marker.get('content', '')[:60]
        print(f"      Content: {content}...")


def demo_repair_plan():
    """Demonstrate repair plan results."""
    print_header("REPAIR PLAN")

    plan_file = Path('repair_plan.json')
    if not plan_file.exists():
        print("⚠ Run: python3 scripts/intelligent_marker_repair.py --analyze")
        return

    with open(plan_file) as f:
        plan = json.load(f)

    summary = plan['summary']

    print(f"\n🎯 Repair Plan Generated: {plan['timestamp']}")
    print(f"\n   Total repairs analyzed: {summary['total_repairs']}")
    print(f"   Safe auto-repairs: {summary['safe_auto']}")
    print(f"   Manual review needed: {summary['needs_review']}")

    print("\n   By Repair Type:")
    for repair_type, count in sorted(summary['by_type'].items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            pct = (count / summary['total_repairs'] * 100) if summary['total_repairs'] else 0
            print(f"      {repair_type:15s} {count:4d} ({pct:5.1f}%)")

    # Show statistics
    stats = plan.get('statistics', {})
    if stats:
        print("\n   Work Distribution:")
        for key, value in sorted(stats.items()):
            if key != 'total_analyzed':
                print(f"      {key:25s} {value:4d}")


def demo_framework_capabilities():
    """Show framework capabilities."""
    print_header("FRAMEWORK CAPABILITIES")

    capabilities = [
        ("🔄 Upstream Sync", "Learn from OpenCog community fixes", "sync_upstream_fixes.py"),
        ("🤖 Intelligent Analysis", "AI-powered repair recommendations", "intelligent_marker_repair.py"),
        ("🔧 Safe Automation", "Apply high-confidence fixes", "Apply with --apply flag"),
        ("📊 Progress Tracking", "Monitor actualization over time", "Weekly re-analysis"),
        ("🎯 Prioritization", "Focus on high-impact repairs", "Severity-based sorting"),
        ("🧪 Dry-Run Mode", "Test before applying", "Always enabled by default"),
    ]

    print("\n✨ Available Features:\n")
    for emoji, feature, details in capabilities:
        print(f"   {emoji}  {feature:25s} - {details}")


def demo_quick_start():
    """Show quick start commands."""
    print_header("QUICK START GUIDE")

    commands = [
        ("1. Run Full Analysis", "python3 scripts/repair_workflow_orchestrator.py"),
        ("2. Sync Upstream", "python3 scripts/sync_upstream_fixes.py --days 30"),
        ("3. Review Plan", "cat repair_plan.json | python3 -m json.tool | less"),
        ("4. Apply Safe Repairs", "python3 scripts/intelligent_marker_repair.py --apply --dry-run"),
    ]

    print("\n🚀 Getting Started:\n")
    for step, command in commands:
        print(f"   {step:20s}")
        print(f"   $ {command}\n")


def demo_metrics():
    """Show key metrics."""
    print_header("ENTELECHY METRICS")

    analysis_file = Path('entelechy_marker_analysis.json')
    if not analysis_file.exists():
        print("⚠ Analysis not available")
        return

    with open(analysis_file) as f:
        data = json.load(f)

    markers = data.get('markers', [])
    total = len(markers)

    # Calculate severity distribution
    critical = sum(1 for m in markers if m.get('severity', 0) >= 0.8)
    high = sum(1 for m in markers if 0.6 <= m.get('severity', 0) < 0.8)
    medium = sum(1 for m in markers if 0.4 <= m.get('severity', 0) < 0.6)
    low = sum(1 for m in markers if m.get('severity', 0) < 0.4)

    print("\n📈 Severity Distribution:\n")
    print(f"   Critical (≥0.8):  {critical:4d} ({critical/total*100:5.1f}%)")
    print(f"   High (0.6-0.8):   {high:4d} ({high/total*100:5.1f}%)")
    print(f"   Medium (0.4-0.6): {medium:4d} ({medium/total*100:5.1f}%)")
    print(f"   Low (<0.4):       {low:4d} ({low/total*100:5.1f}%)")

    # Estimate actualization impact
    fragmentation_density = total / 100000  # markers per 100k LOC (approx)
    actualization_inhibition = min(fragmentation_density * 10, 20)  # max 20%
    current_actualization = 95.3 - actualization_inhibition

    print("\n🧠 Entelechy Assessment:\n")
    print(f"   Current Actualization: {current_actualization:.1f}%")
    print(f"   Fragmentation Density: {fragmentation_density:.2f} per 100k LOC")
    print("   Target Actualization:  >96.0% (transcendent)")
    print(f"   Improvement Needed:    {max(0, 96.0 - current_actualization):.1f}%")


def main():
    """Main demo function."""
    print("\n" + "🧠" * 35)
    print("   ENTELECHY REPAIR FRAMEWORK DEMONSTRATION")
    print("🧠" * 35)

    print(f"\nTimestamp: {datetime.utcnow().isoformat()}Z")
    print(f"Repository: {Path.cwd()}")

    # Run demonstrations
    demo_marker_analysis()
    demo_repair_plan()
    demo_metrics()
    demo_framework_capabilities()
    demo_quick_start()

    # Final notes
    print_header("DOCUMENTATION")
    print("\n📚 Complete guides available:\n")
    print("   • ENTELECHY_REPAIR_WORKFLOW_GUIDE.md")
    print("   • scripts/README.md")
    print("   • repair_plan.json (generated)")
    print("   • entelechy_marker_analysis.json (generated)")

    print("\n" + "=" * 70)
    print("✅ Repair framework ready for systematic actualization")
    print("=" * 70)
    print()


if __name__ == '__main__':
    main()
