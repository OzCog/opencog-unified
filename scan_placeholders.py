#!/usr/bin/env python3
import json
import os
import re


def scan_for_placeholders(root_dir):
    """Scan for actual placeholder implementations that need fixing"""
    placeholders = []

    patterns = {
        'pass_only': re.compile(r'^\s*pass\s*$'),
        'raise_not_implemented': re.compile(r'raise\s+NotImplementedError'),
        'return_none': re.compile(r'^\s*return\s+None\s*$'),
        'empty_function': re.compile(r'{\s*}'),
        'todo_comment': re.compile(r'(//|#)\s*TODO[:\s]*(.*)', re.IGNORECASE),
        'fixme_comment': re.compile(r'(//|#)\s*(XXX\s+)?FIXME[:\s]*(.*)', re.IGNORECASE),
        'stub_function': re.compile(r'(//|#)\s*stub', re.IGNORECASE),
    }

    extensions = ['.py', '.cc', '.cpp', '.h', '.scm']

    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and common build/test directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['build', '__pycache__', 'node_modules']]

        for file in files:
            if not any(file.endswith(ext) for ext in extensions):
                continue

            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, root_dir)

            try:
                with open(filepath, encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                for i, line in enumerate(lines, 1):
                    for pattern_name, pattern in patterns.items():
                        if pattern.search(line):
                            # Get context (3 lines before and after)
                            start = max(0, i-4)
                            end = min(len(lines), i+3)
                            context = ''.join(lines[start:end])

                            placeholders.append({
                                'file': rel_path,
                                'line': i,
                                'type': pattern_name,
                                'content': line.strip(),
                                'context': context
                            })
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

    return placeholders

def categorize_by_priority(placeholders):
    """Categorize placeholders by implementation priority"""
    high_priority = []
    medium_priority = []
    low_priority = []

    for p in placeholders:
        if p['type'] in ['raise_not_implemented', 'pass_only']:
            high_priority.append(p)
        elif p['type'] in ['empty_function', 'stub_function']:
            medium_priority.append(p)
        else:
            low_priority.append(p)

    return {
        'high': high_priority,
        'medium': medium_priority,
        'low': low_priority
    }

if __name__ == '__main__':
    print("Scanning for placeholder implementations...")
    placeholders = scan_for_placeholders('.')
    print(f"Found {len(placeholders)} placeholder instances")

    categorized = categorize_by_priority(placeholders)

    result = {
        'total': len(placeholders),
        'high_priority': len(categorized['high']),
        'medium_priority': len(categorized['medium']),
        'low_priority': len(categorized['low']),
        'by_type': {},
        'categorized': categorized
    }

    # Count by type
    for p in placeholders:
        ptype = p['type']
        result['by_type'][ptype] = result['by_type'].get(ptype, 0) + 1

    with open('placeholder_scan_results.json', 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\nHigh priority: {result['high_priority']}")
    print(f"Medium priority: {result['medium_priority']}")
    print(f"Low priority: {result['low_priority']}")
    print("\nResults saved to placeholder_scan_results.json")
