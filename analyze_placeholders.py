#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path


def analyze_placeholders(root_dir):
    """Scan for all placeholder implementations that need fixing"""

    placeholders = []
    patterns = {
        "FIXME": re.compile(r"(//|#)\s*(XXX\s+)?FIXME[:\s]*(.*)", re.IGNORECASE),
        "TODO": re.compile(r"(//|#)\s*(XXX\s+)?TODO[:\s]*(.*)", re.IGNORECASE),
        "NotImplementedError": re.compile(r"(raise\s+)?NotImplementedError\s*\(?(.*)\)?"),
        "stub": re.compile(r"(//|#)\s*stub[:\s]*(.*)", re.IGNORECASE),
        "pass_placeholder": re.compile(r"pass\s*#\s*placeholder", re.IGNORECASE),
        "empty_function": re.compile(r"^\s*(def|void|int|bool|float|double)\s+\w+\([^)]*\)\s*{\s*}\s*$"),
    }

    extensions = {".cc", ".h", ".cpp", ".hpp", ".py", ".scm", ".c"}

    for root, dirs, files in os.walk(root_dir):
        # Skip hidden and build directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["build", "node_modules", "__pycache__"]]

        for file in files:
            if Path(file).suffix not in extensions:
                continue

            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, root_dir)

            try:
                with open(filepath, encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    for ptype, pattern in patterns.items():
                        match = pattern.search(line)
                        if match:
                            # Get context (3 lines before and after)
                            start = max(0, line_num - 4)
                            end = min(len(lines), line_num + 3)
                            context = "".join(lines[start:end])

                            placeholders.append(
                                {
                                    "file": rel_path,
                                    "line": line_num,
                                    "type": ptype,
                                    "content": line.strip(),
                                    "context": context,
                                    "description": match.group(3) if len(match.groups()) >= 3 else match.group(0),
                                }
                            )
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

    return placeholders


def categorize_placeholders(placeholders):
    """Categorize placeholders by complexity and priority"""

    categories = {
        "critical": [],  # Core functionality blockers
        "high_priority": [],  # Important features
        "medium_priority": [],  # Nice to have
        "low_priority": [],  # Documentation, minor issues
        "informational": [],  # Notes, not actual work items
    }

    critical_keywords = ["crash", "segfault", "memory leak", "deadlock", "race condition", "security"]
    high_keywords = ["implement", "missing", "broken", "bug", "error", "fail"]
    low_keywords = ["optimize", "refactor", "cleanup", "document", "comment"]
    info_keywords = ["note", "see", "reference", "example"]

    for p in placeholders:
        desc = p["description"].lower()
        content = p["content"].lower()

        if any(kw in desc or kw in content for kw in critical_keywords):
            categories["critical"].append(p)
        elif any(kw in desc or kw in content for kw in high_keywords):
            categories["high_priority"].append(p)
        elif any(kw in desc or kw in content for kw in info_keywords):
            categories["informational"].append(p)
        elif any(kw in desc or kw in content for kw in low_keywords):
            categories["low_priority"].append(p)
        else:
            categories["medium_priority"].append(p)

    return categories


def identify_fixable_placeholders(placeholders):
    """Identify placeholders that can be fixed programmatically"""

    fixable = []
    needs_research = []

    for p in placeholders:
        # Check if it's a simple stub or empty function
        if p["type"] in ["stub", "empty_function", "pass_placeholder"]:
            fixable.append({**p, "reason": "Simple stub implementation"})
        # Check if it has clear implementation hints
        elif "implement" in p["description"].lower() and len(p["description"]) > 20:
            fixable.append({**p, "reason": "Has implementation hints"})
        # Check for NotImplementedError with description
        elif p["type"] == "NotImplementedError" and len(p["description"]) > 5:
            fixable.append({**p, "reason": "Error with description"})
        else:
            needs_research.append(p)

    return fixable, needs_research


if __name__ == "__main__":
    print("Analyzing placeholders in opencog-unified...")

    placeholders = analyze_placeholders(".")
    print(f"Found {len(placeholders)} total placeholders")

    # Categorize by priority
    categories = categorize_placeholders(placeholders)
    print("\nBy Priority:")
    for cat, items in categories.items():
        print(f"  {cat}: {len(items)}")

    # Identify fixable items
    fixable, needs_research = identify_fixable_placeholders(placeholders)
    print(f"\nFixable: {len(fixable)}")
    print(f"Needs Research: {len(needs_research)}")

    # Save detailed analysis
    analysis = {
        "total": len(placeholders),
        "by_priority": {k: len(v) for k, v in categories.items()},
        "fixable_count": len(fixable),
        "needs_research_count": len(needs_research),
        "categories": categories,
        "fixable": fixable,
        "needs_research": needs_research,
    }

    with open("detailed_placeholder_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)

    print("\nDetailed analysis saved to detailed_placeholder_analysis.json")
