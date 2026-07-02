#!/usr/bin/env python3
"""
Analyze and categorize the 98 actionable TODO items
"""

import json
from collections import defaultdict


def extract_component(filepath):
    """Extract component name from file path"""
    filepath.split("/")

    # Identify main components
    if "atomspace-storage" in filepath:
        return "atomspace-storage"
    elif "atomspace-restful" in filepath:
        return "atomspace-restful"
    elif "atomspace" in filepath:
        return "atomspace"
    elif "cogserver" in filepath:
        return "cogserver"
    elif "moses" in filepath or "comboreduct" in filepath:
        return "moses"
    elif "ure" in filepath:
        return "ure"
    elif "nlp" in filepath or "lg-" in filepath or "language" in filepath:
        return "nlp"
    elif "eva" in filepath or "chatbot" in filepath:
        return "chatbot"
    elif "integration" in filepath:
        return "integration"
    else:
        return "other"


def estimate_complexity(item):
    """Estimate implementation complexity based on content"""
    content_lower = item["content"].lower()
    context_lower = item.get("context", "").lower()

    # Keywords indicating complexity
    simple_keywords = ["add", "update", "fix typo", "clarify", "document", "comment", "remove"]
    medium_keywords = ["implement", "support", "extend", "replace", "refactor", "improve"]
    complex_keywords = ["algorithm", "optimize", "performance", "thread", "distributed", "cache"]

    # Check for simple tasks
    if any(kw in content_lower for kw in simple_keywords):
        if "hack" in content_lower or "temporary" in content_lower:
            return "medium"
        return "simple"

    # Check for complex tasks
    if any(kw in content_lower or kw in context_lower for kw in complex_keywords):
        return "complex"

    # Check for medium tasks
    if any(kw in content_lower for kw in medium_keywords):
        return "medium"

    # Default to medium
    return "medium"


def estimate_time(complexity, item):
    """Estimate implementation time based on complexity"""
    content = item["content"].lower()

    if complexity == "simple":
        # Simple documentation, comment fixes, or small additions
        if "document" in content or "comment" in content or "clarify" in content:
            return "30min-1hr"
        return "1-2hrs"

    elif complexity == "medium":
        # Feature additions, refactoring, replacements
        if "support" in content or "extend" in content:
            return "4-8hrs"
        elif "replace" in content or "refactor" in content:
            return "8-16hrs"
        return "2-4hrs"

    else:  # complex
        # Algorithm improvements, performance optimization, caching
        if "algorithm" in content or "search" in content:
            return "2-5days"
        elif "cache" in content or "optimize" in content:
            return "1-3days"
        return "3-7days"


def categorize_by_type(item):
    """Categorize TODO by type of work"""
    content_lower = item["content"].lower()

    if "hack" in content_lower or "temporary" in content_lower:
        return "technical_debt"
    elif "support" in content_lower or "add" in content_lower:
        return "feature_addition"
    elif "replace" in content_lower or "nuke" in content_lower:
        return "refactoring"
    elif "implement" in content_lower or "finish" in content_lower:
        return "incomplete_implementation"
    elif "fix" in content_lower or "should be" in content_lower:
        return "bug_fix"
    elif "optimize" in content_lower or "improve" in content_lower:
        return "optimization"
    else:
        return "enhancement"


def analyze_actionable_items():
    """Main analysis function"""

    # Load actionable items
    with open("actionable_items.json") as f:
        items = json.load(f)

    print(f"Analyzing {len(items)} actionable TODO items...\n")

    # Categorize by component
    by_component = defaultdict(list)
    by_complexity = defaultdict(list)
    by_type = defaultdict(list)
    by_time = defaultdict(list)

    # Analyze each item
    analyzed_items = []
    for item in items:
        component = extract_component(item["file"])
        complexity = estimate_complexity(item)
        work_type = categorize_by_type(item)
        time_estimate = estimate_time(complexity, item)

        analyzed = {
            **item,
            "component": component,
            "complexity": complexity,
            "work_type": work_type,
            "time_estimate": time_estimate,
        }

        analyzed_items.append(analyzed)
        by_component[component].append(analyzed)
        by_complexity[complexity].append(analyzed)
        by_type[work_type].append(analyzed)
        by_time[time_estimate].append(analyzed)

    # Generate statistics
    stats = {
        "total_items": len(items),
        "by_component": {k: len(v) for k, v in by_component.items()},
        "by_complexity": {k: len(v) for k, v in by_complexity.items()},
        "by_type": {k: len(v) for k, v in by_type.items()},
        "by_time": {k: len(v) for k, v in by_time.items()},
    }

    # Print summary
    print("=== Component Distribution ===")
    for component, count in sorted(stats["by_component"].items(), key=lambda x: x[1], reverse=True):
        print(f"{component:20s}: {count:3d} items")

    print("\n=== Complexity Distribution ===")
    for complexity, count in sorted(stats["by_complexity"].items(), key=lambda x: x[1], reverse=True):
        print(f"{complexity:20s}: {count:3d} items")

    print("\n=== Work Type Distribution ===")
    for work_type, count in sorted(stats["by_type"].items(), key=lambda x: x[1], reverse=True):
        print(f"{work_type:30s}: {count:3d} items")

    print("\n=== Time Estimate Distribution ===")
    time_order = ["30min-1hr", "1-2hrs", "2-4hrs", "4-8hrs", "8-16hrs", "1-3days", "2-5days", "3-7days"]
    for time_est in time_order:
        if time_est in stats["by_time"]:
            print(f"{time_est:20s}: {stats['by_time'][time_est]:3d} items")

    # Save detailed analysis
    output = {
        "statistics": stats,
        "analyzed_items": analyzed_items,
        "by_component": dict(by_component.items()),
        "by_complexity": dict(by_complexity.items()),
        "by_type": dict(by_type.items()),
        "by_time": dict(by_time.items()),
    }

    with open("actionable_todos_analysis.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\n\nDetailed analysis saved to actionable_todos_analysis.json")

    return output


if __name__ == "__main__":
    analyze_actionable_items()
