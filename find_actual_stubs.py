#!/usr/bin/env python3
"""Find actual stub implementations that need fixing"""

import re
from pathlib import Path


def find_stub_implementations(repo_root):
    """Find functions with only pass, ..., or NotImplementedError"""
    stubs = []

    for pyfile in Path(repo_root).rglob("*.py"):
        # Skip certain directories
        if any(skip in str(pyfile) for skip in [".git", "__pycache__", "_codeql", "build"]):
            continue

        try:
            with open(pyfile, encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.split("\n")

            # Find function definitions followed by stub implementations
            for i, line in enumerate(lines):
                # Match function definitions
                if re.match(r"\s*def\s+\w+\s*\(", line):
                    func_match = re.search(r"def\s+(\w+)\s*\(([^)]*)\)", line)
                    if func_match:
                        func_name = func_match.group(1)
                        func_params = func_match.group(2)

                        # Check next few lines for stub patterns
                        next_lines = lines[i + 1 : min(i + 5, len(lines))]

                        # Skip docstrings
                        start_idx = 0
                        for j, nl in enumerate(next_lines):
                            if '"""' in nl or "'''" in nl:
                                # Find end of docstring
                                for k in range(j + 1, len(next_lines)):
                                    if '"""' in next_lines[k] or "'''" in next_lines[k]:
                                        start_idx = k + 1
                                        break
                                break

                        # Check implementation after docstring
                        impl_lines = next_lines[start_idx:]
                        if impl_lines:
                            first_impl = "\n".join(impl_lines[:3]).strip()

                            # Check for stub patterns
                            is_stub = False
                            stub_type = None

                            if re.match(r"^\s*pass\s*$", first_impl):
                                is_stub = True
                                stub_type = "pass"
                            elif re.match(r"^\s*\.\.\.\s*$", first_impl):
                                is_stub = True
                                stub_type = "ellipsis"
                            elif "raise NotImplementedError" in first_impl:
                                is_stub = True
                                stub_type = "NotImplementedError"
                            elif re.match(r"^\s*return\s+None\s*$", first_impl) and len(impl_lines) == 1:
                                is_stub = True
                                stub_type = "return_none"

                            if is_stub:
                                stubs.append(
                                    {
                                        "file": str(pyfile.relative_to(repo_root)),
                                        "line": i + 1,
                                        "function": func_name,
                                        "params": func_params,
                                        "stub_type": stub_type,
                                        "context": "\n".join(lines[max(0, i - 2) : min(i + 8, len(lines))]),
                                    }
                                )
        except Exception:
            pass

    return stubs


if __name__ == "__main__":
    repo = "/home/ubuntu/opencog-unified"
    print("Scanning for stub implementations...")
    stubs = find_stub_implementations(repo)

    print(f"\nFound {len(stubs)} stub implementations:\n")

    # Group by file
    by_file = {}
    for stub in stubs:
        if stub["file"] not in by_file:
            by_file[stub["file"]] = []
        by_file[stub["file"]].append(stub)

    for filepath, file_stubs in sorted(by_file.items()):
        print(f"\n{filepath}:")
        for stub in file_stubs:
            print(f"  Line {stub['line']}: {stub['function']}({stub['params']}) - {stub['stub_type']}")

    # Save detailed results
    import json

    with open("stub_implementations.json", "w") as f:
        json.dump(stubs, f, indent=2)

    print("\n\nDetailed results saved to stub_implementations.json")
