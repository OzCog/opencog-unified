#!/usr/bin/env python3
"""
Categorize placeholders by implementability
"""
import json


def categorize_by_implementability(placeholders):
    """Categorize placeholders into actionable vs non-actionable"""

    actionable = []
    needs_research = []
    architectural = []
    documentation = []

    for p in placeholders:
        content_lower = p['content'].lower()
        p['file']

        # Documentation issues - easy to fix
        if any(keyword in content_lower for keyword in [
            'document', 'docs', 'comment', 'explain', 'describe',
            'replace below by real docs', 'add description'
        ]):
            documentation.append(p)

        # Architectural/design decisions - need careful consideration
        elif any(keyword in content_lower for keyword in [
            'design', 'architecture', 'refactor', 'rewrite', 'redesign',
            'fundamental', 'major change', 'breaking change'
        ]):
            architectural.append(p)

        # Needs research/investigation
        elif any(keyword in content_lower for keyword in [
            'investigate', 'research', 'unclear', 'not sure', 'figure out',
            'understand', 'someday', 'maybe', 'might', 'performance'
        ]):
            needs_research.append(p)

        # Actionable items
        elif (any(keyword in content_lower for keyword in [
            'implement', 'add', 'create', 'fix', 'complete', 'finish',
            'handle', 'support', 'enable', 'check', 'validate'
        ]) and 'not implemented' not in content_lower) or any(keyword in content_lower for keyword in [
            'remove', 'delete', 'clean up', 'cleanup', 'simplify',
            'temp', 'temporary', 'hack', 'workaround', 'kludge'
        ]):
            actionable.append(p)

        # Default to needs research
        else:
            needs_research.append(p)

    return {
        'actionable': actionable,
        'documentation': documentation,
        'needs_research': needs_research,
        'architectural': architectural
    }

def prioritize_actionable(actionable_items):
    """Prioritize actionable items by ease of implementation"""
    easy = []
    medium = []
    hard = []

    for item in actionable_items:
        content_lower = item['content'].lower()

        # Easy: simple cleanups, removals, documentation
        if any(keyword in content_lower for keyword in [
            'remove', 'delete', 'clean up', 'temp', 'hack', 'workaround',
            'comment', 'document', 'add comment'
        ]):
            easy.append(item)

        # Hard: complex implementations
        elif any(keyword in content_lower for keyword in [
            'algorithm', 'optimize', 'performance', 'thread', 'concurrent',
            'parallel', 'distributed', 'cache', 'memory'
        ]):
            hard.append(item)

        # Medium: everything else
        else:
            medium.append(item)

    return {'easy': easy, 'medium': medium, 'hard': hard}

if __name__ == '__main__':
    # Load placeholder analysis
    with open('placeholder_analysis.json') as f:
        data = json.load(f)

    placeholders = data['detailed_placeholders']

    # Categorize
    categories = categorize_by_implementability(placeholders)

    # Prioritize actionable
    actionable_priority = prioritize_actionable(categories['actionable'])

    # Generate report
    report = {
        'summary': {
            'total': len(placeholders),
            'actionable': len(categories['actionable']),
            'documentation': len(categories['documentation']),
            'needs_research': len(categories['needs_research']),
            'architectural': len(categories['architectural']),
            'easy_fixes': len(actionable_priority['easy']),
            'medium_fixes': len(actionable_priority['medium']),
            'hard_fixes': len(actionable_priority['hard'])
        },
        'categories': categories,
        'actionable_priority': actionable_priority
    }

    # Save report
    with open('placeholder_categorization.json', 'w') as f:
        json.dump(report, f, indent=2)

    print("Placeholder Categorization Report")
    print("=" * 50)
    print(f"Total Placeholders: {report['summary']['total']}")
    print(f"\nActionable: {report['summary']['actionable']}")
    print(f"  - Easy fixes: {report['summary']['easy_fixes']}")
    print(f"  - Medium fixes: {report['summary']['medium_fixes']}")
    print(f"  - Hard fixes: {report['summary']['hard_fixes']}")
    print(f"\nDocumentation: {report['summary']['documentation']}")
    print(f"Needs Research: {report['summary']['needs_research']}")
    print(f"Architectural: {report['summary']['architectural']}")

    print("\n\nTop 20 Easy Fixes:")
    for i, item in enumerate(actionable_priority['easy'][:20], 1):
        print(f"{i}. {item['file']}:{item['line']}")
        print(f"   {item['content'][:80]}")
