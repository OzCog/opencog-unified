#!/usr/bin/env python3
"""
Test script to validate that the comprehensive TODO catalog includes all required items
from the problem statement.
"""

import os
import sys


def test_catalog_contains_required_items():
    """Test that the catalog contains the specific items mentioned in the problem statement"""

    catalog_path = 'COMPREHENSIVE-TODO-CATALOG.md'
    if not os.path.exists(catalog_path):
        print("❌ COMPREHENSIVE-TODO-CATALOG.md not found")
        return False

    with open(catalog_path) as f:
        content = f.read()

    # Required items from the problem statement
    required_items = [
        'BackingStore.h',  # Persistence Subsystem
        'representation/build_knobs.cc',  # MOSES Representation
        'scoring_base.cc', # MOSES Scoring
        'table.h',         # MOSES Table
    ]

    # Specific TODO items that must exist
    required_todo_patterns = [
        'atomspace-storage/opencog/persist/api/BackingStore.h',  # BackingStore TODO items
        'moses/scoring/bscores.h',  # MOSES scoring TODO items
    ]

    missing_items = []
    for item in required_items:
        if item not in content:
            missing_items.append(item)

    # Check for specific TODO patterns
    missing_todo_patterns = []
    for pattern in required_todo_patterns:
        if pattern not in content:
            missing_todo_patterns.append(pattern)

    if missing_items:
        print(f"❌ Missing required items: {missing_items}")
        return False

    if missing_todo_patterns:
        print(f"❌ Missing required TODO patterns: {missing_todo_patterns}")
        return False

    # Check structure requirements
    required_sections = [
        '# Cognitive Flowchart: Comprehensive TODO Enumeration',
        '## 1. Subsystem Mapping',
        '## 2. Pattern Recognition',
        '## 3. Recursive Solution Design',
        '## 4. Meta-Cognitive Enhancement',
        '## 5. Theatrical Finale',
        '## Outstanding Items',
        '### Persistence Subsystem',
        '### MOSES Representation/Scoring',
        'Let us converge upon a state of sublime implementation',
        'ref: 25d11bfe332cd501a967d9ab3a6957a22504249f'
    ]

    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)

    if missing_sections:
        print(f"❌ Missing required sections: {missing_sections}")
        return False

    print("✅ All required items and sections found in the catalog")
    return True

def test_catalog_statistics():
    """Test that the catalog has reasonable statistics"""

    catalog_path = 'COMPREHENSIVE-TODO-CATALOG.md'
    with open(catalog_path) as f:
        content = f.read()

    # Count checkboxes (should be many)
    checkbox_count = content.count('- [ ]')
    if checkbox_count < 700:  # Should have hundreds of TODOs (current catalog has ~823)
        print(f"❌ Too few TODO items found: {checkbox_count}, expected at least 700")
        return False

    # Check for GitHub links
    github_link_count = content.count('github.com/OzCog/opencog-unified/blob/')
    if github_link_count < 700:  # Should have many GitHub links (similar to TODO count)
        print(f"❌ Too few GitHub links found: {github_link_count}, expected at least 700")
        return False

    print(f"✅ Found {checkbox_count} TODO items with {github_link_count} GitHub links")
    return True

def main():
    """Run all tests"""
    print("🧪 Testing comprehensive TODO catalog...")

    tests = [
        test_catalog_contains_required_items,
        test_catalog_statistics,
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    if all_passed:
        print("🎉 All tests passed! The comprehensive TODO catalog is properly generated.")
        return 0
    else:
        print("❌ Some tests failed.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
