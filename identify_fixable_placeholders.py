#!/usr/bin/env python3
import json
import os
import re


def load_scan_results():
    with open("placeholder_scan_results.json") as f:
        return json.load(f)


def is_exception_handler(context):
    """Check if pass is in exception handler (legitimate use)"""
    return "except" in context and context.strip().endswith("pass")


def is_empty_init(context):
    """Check if it's an empty __init__ (sometimes legitimate)"""
    return "def __init__" in context


def filter_legitimate_passes(high_priority):
    """Filter out legitimate uses of pass"""
    fixable = []
    legitimate = []

    for item in high_priority:
        if item["type"] == "pass_only":
            # Exception handlers are often legitimate
            if is_exception_handler(item["context"]):
                legitimate.append(item)
                continue
            # Empty __init__ might be legitimate
            if is_empty_init(item["context"]):
                legitimate.append(item)
                continue

        fixable.append(item)

    return fixable, legitimate


def identify_actual_stubs():
    """Find actual stub functions that need implementation"""
    stubs = []

    # Look for functions with only pass or return None
    for root, dirs, files in os.walk("."):
        # Skip hidden and build directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["build", "__pycache__"]]

        for file in files:
            if not file.endswith(".py"):
                continue

            filepath = os.path.join(root, file)
            try:
                with open(filepath, encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    lines = content.split("\n")

                # Find function definitions
                for i, line in enumerate(lines):
                    if re.match(r"^\s*def\s+\w+\s*\(", line):
                        # Look ahead to see if it's just pass or return None
                        match = re.search(r"def\s+(\w+)", line)
                        if not match:
                            continue
                        func_name = match.group(1)

                        # Skip private methods and test methods
                        if func_name.startswith("_") or func_name.startswith("test_"):
                            continue

                        # Check next few lines
                        impl_lines = []
                        for j in range(i + 1, min(i + 10, len(lines))):
                            stripped = lines[j].strip()
                            if stripped and not stripped.startswith("#") and not stripped.startswith('"""'):
                                impl_lines.append(stripped)
                                if not stripped.endswith(",") and not stripped.endswith("\\"):
                                    break

                        # Check if it's a stub
                        if len(impl_lines) == 1:
                            first = impl_lines[0]
                            if first in {"pass", "return None"} or "NotImplementedError" in first:
                                stubs.append(
                                    {
                                        "file": filepath,
                                        "line": i + 1,
                                        "function": func_name,
                                        "type": "stub_function",
                                        "implementation": first,
                                    }
                                )
            except Exception:
                pass

    return stubs


if __name__ == "__main__":
    results = load_scan_results()
    high_priority = results["categorized"]["high"]

    print(f"Total high priority items: {len(high_priority)}")

    fixable, legitimate = filter_legitimate_passes(high_priority)
    print(f"Fixable items: {len(fixable)}")
    print(f"Legitimate passes (exception handlers, etc.): {len(legitimate)}")

    # Find actual stub functions
    stubs = identify_actual_stubs()
    print(f"Actual stub functions found: {len(stubs)}")

    output = {
        "fixable_high_priority": fixable,
        "legitimate_passes": legitimate,
        "stub_functions": stubs,
        "summary": {
            "total_high_priority": len(high_priority),
            "fixable": len(fixable),
            "legitimate": len(legitimate),
            "stub_functions": len(stubs),
        },
    }

    with open("fixable_placeholders.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\nResults saved to fixable_placeholders.json")
