#!/usr/bin/env python3
"""
Analyze C++ FIXME/TODO comments to identify which ones can be addressed
"""

import json
import os


fixmes = []

# Scan C++ files
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["build", "__pycache__"]]

    for file in files:
        if not (file.endswith(".cc") or file.endswith(".h") or file.endswith(".cpp")):
            continue

        filepath = os.path.join(root, file)
        try:
            with open(filepath, encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                if "XXX FIXME" in line or "TODO FIXME" in line:
                    # Get context
                    start = max(0, i - 3)
                    end = min(len(lines), i + 3)
                    context = "".join(lines[start:end])

                    fixmes.append({"file": filepath, "line": i, "content": line.strip(), "context": context})
        except Exception:
            pass

print(f"Found {len(fixmes)} C++ FIXME/TODO comments")

# Categorize by type
categories = {
    "thread_safety": [],
    "optimization": [],
    "error_handling": [],
    "documentation": [],
    "refactoring": [],
    "feature_incomplete": [],
    "other": [],
}

for fixme in fixmes:
    content_lower = fixme["content"].lower()

    if "thread" in content_lower or "lock" in content_lower or "race" in content_lower:
        categories["thread_safety"].append(fixme)
    elif "optim" in content_lower or "performance" in content_lower or "slow" in content_lower:
        categories["optimization"].append(fixme)
    elif "error" in content_lower or "exception" in content_lower or "throw" in content_lower:
        categories["error_handling"].append(fixme)
    elif "document" in content_lower or "comment" in content_lower:
        categories["documentation"].append(fixme)
    elif "refactor" in content_lower or "clean" in content_lower or "rewrite" in content_lower:
        categories["refactoring"].append(fixme)
    elif "not implemented" in content_lower or "implement" in content_lower or "stub" in content_lower:
        categories["feature_incomplete"].append(fixme)
    else:
        categories["other"].append(fixme)

print("\nCategories:")
for cat, items in categories.items():
    print(f"  {cat}: {len(items)}")

# Save results
output = {
    "total": len(fixmes),
    "categories": {k: len(v) for k, v in categories.items()},
    "fixmes_by_category": categories,
}

with open("cpp_fixme_analysis.json", "w") as f:
    json.dump(output, f, indent=2)

print("\nAnalysis saved to cpp_fixme_analysis.json")

# Show some examples of feature_incomplete
if categories["feature_incomplete"]:
    print("\n=== Feature Incomplete Examples ===")
    for item in categories["feature_incomplete"][:5]:
        print(f"\n{item['file']}:{item['line']}")
        print(f"  {item['content']}")
