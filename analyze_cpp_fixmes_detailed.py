#!/usr/bin/env python3
"""
Detailed C++ FIXME Analysis Script
Categorizes FIXMEs by severity, module, and impact
"""

import json
from collections import defaultdict
from pathlib import Path


def extract_module_from_path(filepath):
    """Extract module name from file path"""
    parts = Path(filepath).parts

    # Skip leading ./ and find the main module
    for i, part in enumerate(parts):
        if part in ['.', '..']:
            continue
        # First meaningful directory is usually the module
        if i < len(parts) - 1:  # Not the filename itself
            return part
    return 'unknown'

def categorize_severity(fixme_content, context):
    """
    Categorize FIXME by severity based on keywords and context
    Returns: (severity, category, description)
    """
    content_lower = (fixme_content + context).lower()

    # CRITICAL: Security, crashes, data loss, undefined behavior
    if any(kw in content_lower for kw in [
        'crash', 'segfault', 'undefined behavior', 'memory leak',
        'security', 'vulnerability', 'data loss', 'corruption',
        'race condition', 'deadlock', 'buffer overflow'
    ]):
        return 'CRITICAL', 'security_or_crash', 'Security vulnerability or crash risk'

    # HIGH: Thread safety, exception handling, API correctness
    if any(kw in content_lower for kw in [
        'thread', 'lock', 'mutex', 'atomic', 'concurrent',
        'exception', 'throw', 'error handling', 'catch'
    ]):
        if 'throw' in content_lower or 'exception' in content_lower:
            return 'HIGH', 'exception_handling', 'Exception/error handling issue'
        return 'HIGH', 'thread_safety', 'Thread safety or concurrency issue'

    # HIGH: Performance bottlenecks
    if any(kw in content_lower for kw in [
        'performance', 'slow', 'bottleneck', 'optimize', 'inefficient'
    ]):
        return 'HIGH', 'performance', 'Performance optimization needed'

    # MEDIUM: Incomplete features, API design
    if any(kw in content_lower for kw in [
        'incomplete', 'not implemented', 'todo', 'missing',
        'should be', 'need to', 'must'
    ]):
        return 'MEDIUM', 'incomplete_feature', 'Incomplete implementation'

    # MEDIUM: Code quality issues
    if any(kw in content_lower for kw in [
        'hack', 'workaround', 'temporary', 'kludge', 'cheesy',
        'ugly', 'messy', 'cleanup', 'refactor'
    ]):
        return 'MEDIUM', 'code_quality', 'Code quality/refactoring needed'

    # MEDIUM: API design issues
    if any(kw in content_lower for kw in [
        'api', 'interface', 'design', 'architecture', 'structure'
    ]):
        return 'MEDIUM', 'api_design', 'API or design improvement'

    # LOW: Documentation, comments
    if any(kw in content_lower for kw in [
        'document', 'comment', 'explain', 'clarify'
    ]):
        return 'LOW', 'documentation', 'Documentation needed'

    # LOW: General improvements
    return 'LOW', 'general', 'General improvement or consideration'

def analyze_fixmes():
    """Analyze all C++ FIXMEs with detailed categorization"""

    # Load the existing analysis
    with open('cpp_fixme_analysis.json') as f:
        data = json.load(f)

    # Detailed analysis structure
    analysis = {
        'total': data['total'],
        'by_severity': defaultdict(list),
        'by_module': defaultdict(list),
        'by_category': defaultdict(list),
        'summary': {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        },
        'module_summary': defaultdict(lambda: {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}),
        'category_summary': defaultdict(int)
    }

    # Process all FIXMEs from all categories
    all_fixmes = []
    for category, fixmes in data['fixmes_by_category'].items():
        all_fixmes.extend(fixmes)

    # Analyze each FIXME
    for fixme in all_fixmes:
        filepath = fixme['file']
        content = fixme['content']
        context = fixme.get('context', '')
        line = fixme['line']

        # Extract module
        module = extract_module_from_path(filepath)

        # Categorize severity
        severity, category, description = categorize_severity(content, context)

        # Create detailed entry
        entry = {
            'file': filepath,
            'line': line,
            'module': module,
            'severity': severity,
            'category': category,
            'description': description,
            'content': content.strip(),
            'context_preview': context.strip()[:200] + '...' if len(context.strip()) > 200 else context.strip()
        }

        # Add to categorizations
        analysis['by_severity'][severity].append(entry)
        analysis['by_module'][module].append(entry)
        analysis['by_category'][category].append(entry)

        # Update summaries
        analysis['summary'][severity.lower()] += 1
        analysis['module_summary'][module][severity.lower()] += 1
        analysis['category_summary'][category] += 1

    # Convert defaultdicts to regular dicts for JSON serialization
    analysis['by_severity'] = dict(analysis['by_severity'])
    analysis['by_module'] = dict(analysis['by_module'])
    analysis['by_category'] = dict(analysis['by_category'])
    analysis['module_summary'] = dict(analysis['module_summary'])
    analysis['category_summary'] = dict(analysis['category_summary'])

    # Sort by severity
    for severity in analysis['by_severity']:
        analysis['by_severity'][severity].sort(key=lambda x: (x['module'], x['file'], x['line']))

    # Save detailed analysis
    with open('cpp_fixme_detailed_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)

    return analysis

def generate_report(analysis):
    """Generate a human-readable report"""

    report = []
    report.append("=" * 80)
    report.append("C++ FIXME DETAILED ANALYSIS REPORT")
    report.append("=" * 80)
    report.append("")

    # Summary
    report.append("SEVERITY SUMMARY")
    report.append("-" * 80)
    report.append(f"CRITICAL: {analysis['summary']['critical']:3d} - Security, crashes, undefined behavior")
    report.append(f"HIGH:     {analysis['summary']['high']:3d} - Thread safety, exceptions, performance")
    report.append(f"MEDIUM:   {analysis['summary']['medium']:3d} - Incomplete features, code quality")
    report.append(f"LOW:      {analysis['summary']['low']:3d} - Documentation, general improvements")
    report.append(f"TOTAL:    {analysis['total']:3d}")
    report.append("")

    # Module summary
    report.append("MODULE SUMMARY")
    report.append("-" * 80)
    report.append(f"{'Module':<30} {'Critical':>8} {'High':>8} {'Medium':>8} {'Low':>8} {'Total':>8}")
    report.append("-" * 80)

    module_totals = []
    for module, counts in analysis['module_summary'].items():
        total = sum(counts.values())
        module_totals.append((module, counts, total))

    # Sort by total descending
    module_totals.sort(key=lambda x: x[2], reverse=True)

    for module, counts, total in module_totals:
        report.append(f"{module:<30} {counts['critical']:8d} {counts['high']:8d} {counts['medium']:8d} {counts['low']:8d} {total:8d}")

    report.append("")

    # Category summary
    report.append("CATEGORY SUMMARY")
    report.append("-" * 80)
    report.append(f"{'Category':<30} {'Count':>8}")
    report.append("-" * 80)

    for category, count in sorted(analysis['category_summary'].items(), key=lambda x: x[1], reverse=True):
        report.append(f"{category:<30} {count:8d}")

    report.append("")

    # Top priority items (CRITICAL and HIGH)
    report.append("TOP PRIORITY ITEMS (CRITICAL & HIGH)")
    report.append("=" * 80)

    priority_items = []
    if 'CRITICAL' in analysis['by_severity']:
        priority_items.extend(analysis['by_severity']['CRITICAL'])
    if 'HIGH' in analysis['by_severity']:
        priority_items.extend(analysis['by_severity']['HIGH'])

    for i, item in enumerate(priority_items[:20], 1):  # Top 20
        report.append("")
        report.append(f"{i}. [{item['severity']}] {item['category']}")
        report.append(f"   Module: {item['module']}")
        report.append(f"   File: {item['file']}:{item['line']}")
        report.append(f"   Description: {item['description']}")
        report.append(f"   Content: {item['content']}")

    if len(priority_items) > 20:
        report.append("")
        report.append(f"... and {len(priority_items) - 20} more priority items")

    report.append("")
    report.append("=" * 80)
    report.append("Full details available in: cpp_fixme_detailed_analysis.json")
    report.append("=" * 80)

    return "\n".join(report)

if __name__ == '__main__':
    print("Analyzing C++ FIXMEs in detail...")
    analysis = analyze_fixmes()

    report = generate_report(analysis)

    # Save report
    with open('cpp_fixme_analysis_report.txt', 'w') as f:
        f.write(report)

    print(report)
    print("\nAnalysis complete!")
    print("- Detailed JSON: cpp_fixme_detailed_analysis.json")
    print("- Human report: cpp_fixme_analysis_report.txt")
