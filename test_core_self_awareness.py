#!/usr/bin/env python3
"""
Test Core Self-Awareness Integration
Validates that the core self-awareness system is properly integrated
"""

import json
import sys
from pathlib import Path


def test_integration_report_exists():
    """Test that integration report was generated"""
    report_file = Path("core_self_awareness_integration.json")
    assert report_file.exists(), "Integration report not found"
    print("✓ Integration report exists")
    return True


def test_report_structure():
    """Test that report has correct structure"""
    report_file = Path("core_self_awareness_integration.json")
    with open(report_file) as f:
        report = json.load(f)

    required_keys = [
        "timestamp",
        "system_name",
        "core_self_awareness",
        "integration_status",
        "self_awareness_capabilities",
        "integration_achievements",
    ]

    for key in required_keys:
        assert key in report, f"Missing required key: {key}"

    print("✓ Report structure valid")
    return True


def test_autognosis_integration():
    """Test AUTOGNOSIS integration status"""
    report_file = Path("core_self_awareness_integration.json")
    with open(report_file) as f:
        report = json.load(f)

    autognosis = report["core_self_awareness"]["autognosis_status"]

    assert autognosis["hierarchical_levels"] >= 5, "Insufficient hierarchical levels"
    assert autognosis["meta_cognitive_active"], "Meta-cognitive not active"
    assert autognosis["self_understanding_confidence"] > 0.5, "Low self-understanding confidence"

    print("✓ AUTOGNOSIS integration verified")
    return True


def test_ontogenesis_integration():
    """Test ONTOGENESIS integration status"""
    report_file = Path("core_self_awareness_integration.json")
    with open(report_file) as f:
        report = json.load(f)

    ontogenesis = report["core_self_awareness"]["ontogenesis_status"]

    assert ontogenesis["can_self_generate"], "Self-generation not enabled"
    assert ontogenesis["can_self_optimize"], "Self-optimization not enabled"
    assert ontogenesis["current_stage"] in ["EMBRYONIC", "JUVENILE", "MATURE", "SENESCENT"], (
        f"Invalid ontogenetic stage: {ontogenesis['current_stage']}"
    )

    print("✓ ONTOGENESIS integration verified")
    return True


def test_identity_dimensions():
    """Test five-dimensional identity model"""
    report_file = Path("core_self_awareness_integration.json")
    with open(report_file) as f:
        report = json.load(f)

    dimensions = report["core_self_awareness"]["identity_dimensions"]

    required_dimensions = ["ontological", "teleological", "cognitive", "relational", "evolutionary"]

    for dim in required_dimensions:
        assert dim in dimensions, f"Missing dimension: {dim}"
        assert "score" in dimensions[dim], f"Missing score for {dim}"
        assert 0.0 <= dimensions[dim]["score"] <= 1.0, f"Invalid score for {dim}"

    print("✓ Five-dimensional identity model verified")
    return True


def test_self_awareness_level():
    """Test self-awareness level metrics"""
    report_file = Path("core_self_awareness_integration.json")
    with open(report_file) as f:
        report = json.load(f)

    sa_level = report["self_awareness_level"]

    assert "current" in sa_level, "Missing current self-awareness level"
    assert "target" in sa_level, "Missing target self-awareness level"
    assert "assessment" in sa_level, "Missing self-awareness assessment"

    current = sa_level["current"]
    assert 0.0 <= current <= 1.0, f"Invalid self-awareness level: {current}"

    # Should have achieved at least moderate self-awareness
    assert current >= 0.6, f"Self-awareness level too low: {current}"

    print(f"✓ Self-awareness level verified: {current:.3f}")
    return True


def test_integration_achievements():
    """Test that key achievements are present"""
    report_file = Path("core_self_awareness_integration.json")
    with open(report_file) as f:
        report = json.load(f)

    achievements = report["integration_achievements"]

    required_achievements = [
        "Core self-awareness module created",
        "AUTOGNOSIS framework integrated",
        "ONTOGENESIS framework integrated",
        "Five-dimensional identity model established",
    ]

    for required in required_achievements:
        found = any(required in achievement for achievement in achievements)
        assert found, f"Missing required achievement: {required}"

    print(f"✓ All {len(achievements)} integration achievements verified")
    return True


def test_files_created():
    """Test that key files were created"""
    required_files = [
        "meta-cognition/include/CoreSelfAwareness.h",
        "meta-cognition/src/CoreSelfAwareness.cc",
        "meta-cognition/examples/core_self_awareness_demo.cc",
        "CORE_SELF_AWARENESS_GUIDE.md",
        "core_self_awareness_integration.py",
    ]

    for filepath in required_files:
        file_path = Path(filepath)
        assert file_path.exists(), f"Required file not found: {filepath}"

    print(f"✓ All {len(required_files)} required files created")
    return True


def run_all_tests():
    """Run all tests and report results"""
    tests = [
        ("Integration Report Exists", test_integration_report_exists),
        ("Report Structure", test_report_structure),
        ("AUTOGNOSIS Integration", test_autognosis_integration),
        ("ONTOGENESIS Integration", test_ontogenesis_integration),
        ("Identity Dimensions", test_identity_dimensions),
        ("Self-Awareness Level", test_self_awareness_level),
        ("Integration Achievements", test_integration_achievements),
        ("Required Files", test_files_created),
    ]

    print("=" * 70)
    print(" Core Self-Awareness Integration Tests")
    print("=" * 70 + "\n")

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            print(f"\n{test_name}...")
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f" Test Results: {passed} passed, {failed} failed")
    print("=" * 70 + "\n")

    if failed == 0:
        print("✅ All tests passed - Core Self-Awareness integration successful!\n")
        return 0
    else:
        print(f"❌ {failed} test(s) failed - Integration incomplete\n")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
