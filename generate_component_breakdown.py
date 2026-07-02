#!/usr/bin/env python3
"""
Generate detailed component breakdown with priorities
"""

import json
from collections import defaultdict


def generate_component_breakdown():
    """Generate detailed breakdown by component"""

    with open("actionable_todos_analysis.json") as f:
        analysis = json.load(f)

    by_component = analysis["by_component"]

    print("=" * 80)
    print("DETAILED COMPONENT BREAKDOWN")
    print("=" * 80)

    # Sort components by item count
    sorted_components = sorted(by_component.items(), key=lambda x: len(x[1]), reverse=True)

    for component, items in sorted_components:
        print(f"\n{'=' * 80}")
        print(f"COMPONENT: {component.upper()}")
        print(f"Total Items: {len(items)}")
        print(f"{'=' * 80}")

        # Group by complexity
        by_complexity = defaultdict(list)
        for item in items:
            by_complexity[item["complexity"]].append(item)

        # Show complexity distribution
        print("\nComplexity Distribution:")
        for complexity in ["simple", "medium", "complex"]:
            if complexity in by_complexity:
                count = len(by_complexity[complexity])
                print(f"  {complexity.capitalize():10s}: {count:2d} items")

        # Show time estimates
        time_totals = defaultdict(int)
        for item in items:
            time_totals[item["time_estimate"]] += 1

        print("\nTime Estimates:")
        for time_est, count in sorted(time_totals.items()):
            print(f"  {time_est:15s}: {count:2d} items")

        # Show work types
        work_types = defaultdict(int)
        for item in items:
            work_types[item["work_type"]] += 1

        print("\nWork Types:")
        for work_type, count in sorted(work_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {work_type:30s}: {count:2d} items")

        # Show top priority items (simple complexity or quick wins)
        quick_wins = [
            item for item in items if item["complexity"] == "simple" or item["time_estimate"] in ["30min-1hr", "1-2hrs"]
        ]

        if quick_wins:
            print(f"\n  Quick Wins ({len(quick_wins)} items):")
            for item in quick_wins[:5]:
                print(f"    - {item['file']}:{item['line']}")
                print(f"      {item['content'][:70]}...")
                print(f"      Time: {item['time_estimate']}, Type: {item['work_type']}")

        # Show sample items
        print("\n  Sample Items:")
        for i, item in enumerate(items[:3], 1):
            print(f"\n    {i}. {item['file']}:{item['line']}")
            print(f"       {item['content'][:70]}...")
            print(f"       Complexity: {item['complexity']}, Time: {item['time_estimate']}")
            print(f"       Type: {item['work_type']}")

    print("\n" + "=" * 80)


def generate_priority_recommendations():
    """Generate priority recommendations"""

    with open("actionable_todos_analysis.json") as f:
        analysis = json.load(f)

    items = analysis["analyzed_items"]

    print("\n" + "=" * 80)
    print("PRIORITY RECOMMENDATIONS")
    print("=" * 80)

    # Priority 1: Quick wins (simple, fast)
    quick_wins = [
        item for item in items if item["complexity"] == "simple" or item["time_estimate"] in ["30min-1hr", "1-2hrs"]
    ]

    print(f"\n1. QUICK WINS (Priority 1) - {len(quick_wins)} items")
    print("   These can be completed in 1-2 hours each")
    print("   Recommended: Start here to build momentum\n")

    by_component = defaultdict(list)
    for item in quick_wins:
        by_component[item["component"]].append(item)

    for component, comp_items in sorted(by_component.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {component}: {len(comp_items)} items")

    # Priority 2: Bug fixes (medium complexity)
    bug_fixes = [
        item
        for item in items
        if item["work_type"] == "bug_fix"
        and item["complexity"] == "medium"
        and item["time_estimate"] in ["2-4hrs", "4-8hrs"]
    ]

    print(f"\n2. BUG FIXES (Priority 2) - {len(bug_fixes)} items")
    print("   Medium complexity bug fixes")
    print("   Recommended: Tackle after quick wins\n")

    by_component = defaultdict(list)
    for item in bug_fixes:
        by_component[item["component"]].append(item)

    for component, comp_items in sorted(by_component.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {component}: {len(comp_items)} items")

    # Priority 3: Feature additions
    features = [item for item in items if item["work_type"] == "feature_addition"]

    print(f"\n3. FEATURE ADDITIONS (Priority 3) - {len(features)} items")
    print("   New features and support additions")
    print("   Recommended: After bug fixes are addressed\n")

    by_component = defaultdict(list)
    for item in features:
        by_component[item["component"]].append(item)

    for component, comp_items in sorted(by_component.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {component}: {len(comp_items)} items")

    # Priority 4: Refactoring and technical debt
    refactoring = [item for item in items if item["work_type"] in ["refactoring", "technical_debt"]]

    print(f"\n4. REFACTORING & TECHNICAL DEBT (Priority 4) - {len(refactoring)} items")
    print("   Code quality improvements")
    print("   Recommended: Schedule as part of regular maintenance\n")

    by_component = defaultdict(list)
    for item in refactoring:
        by_component[item["component"]].append(item)

    for component, comp_items in sorted(by_component.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {component}: {len(comp_items)} items")

    # Priority 5: Complex items
    complex_items = [item for item in items if item["complexity"] == "complex"]

    print(f"\n5. COMPLEX ITEMS (Priority 5) - {len(complex_items)} items")
    print("   Require significant time and expertise")
    print("   Recommended: Plan carefully, may need specialist knowledge\n")

    for item in complex_items:
        print(f"   - {item['component']}: {item['file']}:{item['line']}")
        print(f"     {item['content'][:60]}...")
        print(f"     Time: {item['time_estimate']}\n")

    print("=" * 80)


if __name__ == "__main__":
    generate_component_breakdown()
    generate_priority_recommendations()
