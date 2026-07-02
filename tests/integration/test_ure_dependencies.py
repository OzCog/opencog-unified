#!/usr/bin/env python3
"""
Test script to verify that URE component properly declares and finds its dependencies.
This test focuses on the CMake configuration and dependency resolution.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, capture_output=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=capture_output, text=True, timeout=300)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def test_ure_dependencies():
    """Test that URE properly declares its dependencies in its config file."""
    print("Testing URE dependency declarations...")

    # Find the URE config template
    ure_config = Path(__file__).parent.parent.parent / "ure" / "lib" / "UREConfig.cmake.in"

    if not ure_config.exists():
        print(f"ERROR: URE config template not found at {ure_config}")
        return False

    # Read the config file and check for dependency declarations
    content = ure_config.read_text()

    required_patterns = [
        "include(CMakeFindDependencyMacro)",
        "find_dependency(CogUtil CONFIG REQUIRED)",
        "find_dependency(AtomSpace CONFIG REQUIRED)",
        "find_dependency(Unify CONFIG REQUIRED)",
    ]

    missing_patterns = []
    for pattern in required_patterns:
        if pattern not in content:
            missing_patterns.append(pattern)

    if missing_patterns:
        print("ERROR: Missing dependency declarations in UREConfig.cmake.in:")
        for pattern in missing_patterns:
            print(f"  - {pattern}")
        return False

    print("SUCCESS: URE config properly declares dependencies on CogUtil, AtomSpace, and Unify")
    return True


def test_unify_dependencies():
    """Test that Unify properly declares its dependencies in its config file."""
    print("Testing Unify dependency declarations...")

    # Find the Unify config template
    unify_config = Path(__file__).parent.parent.parent / "unify" / "lib" / "UnifyConfig.cmake.in"

    if not unify_config.exists():
        print(f"ERROR: Unify config template not found at {unify_config}")
        return False

    # Read the config file and check for dependency declarations
    content = unify_config.read_text()

    required_patterns = [
        "include(CMakeFindDependencyMacro)",
        "find_dependency(CogUtil CONFIG REQUIRED)",
        "find_dependency(AtomSpace CONFIG REQUIRED)",
    ]

    missing_patterns = []
    for pattern in required_patterns:
        if pattern not in content:
            missing_patterns.append(pattern)

    if missing_patterns:
        print("ERROR: Missing dependency declarations in UnifyConfig.cmake.in:")
        for pattern in missing_patterns:
            print(f"  - {pattern}")
        return False

    print("SUCCESS: Unify config properly declares dependencies on CogUtil and AtomSpace")
    return True


def test_cmake_dependency_order():
    """Test that the main CMakeLists.txt has proper dependency order."""
    print("Testing CMake dependency order...")

    # Find the main CMakeLists.txt
    main_cmake = Path(__file__).parent.parent.parent / "CMakeLists.txt"

    if not main_cmake.exists():
        print(f"ERROR: Main CMakeLists.txt not found at {main_cmake}")
        return False

    content = main_cmake.read_text()

    # Check that dependencies are set up correctly
    expected_deps = ["add_dependencies(unify atomspace)", "add_dependencies(ure unify)"]

    missing_deps = []
    for dep in expected_deps:
        if dep not in content:
            missing_deps.append(dep)

    if missing_deps:
        print("ERROR: Missing dependency declarations in main CMakeLists.txt:")
        for dep in missing_deps:
            print(f"  - {dep}")
        return False

    print("SUCCESS: Main CMakeLists.txt has proper dependency order")
    return True


def main():
    """Main test function."""
    print("=" * 60)
    print("URE DEPENDENCY CONFIGURATION TEST")
    print("=" * 60)

    tests = [test_ure_dependencies, test_unify_dependencies, test_cmake_dependency_order]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"ERROR: Test {test.__name__} failed with exception: {e}")
            print()

    print("=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("SUCCESS: All URE dependency tests passed!")
        return 0
    else:
        print("FAILURE: Some URE dependency tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
