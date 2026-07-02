#!/usr/bin/env python3
"""
Integration test for unify atomspace dependency declaration
"""

import os
import sys


def test_unify_dependency():
    """Test that unify properly requires atomspace"""

    # Test 1: Verify unify CMakeLists.txt declares atomspace dependency
    cmake_file = "/home/runner/work/opencog-unified/opencog-unified/unify/CMakeLists.txt"

    with open(cmake_file) as f:
        content = f.read()

    assert "find_package(AtomSpace" in content or "IF(TARGET atomspace)" in content, (
        "unify must declare AtomSpace dependency"
    )
    assert "HAVE_ATOMSPACE" in content, "unify must check for HAVE_ATOMSPACE"
    assert "unify requires: atomspace" in content, "unify must explicitly declare atomspace requirement"
    print("✅ unify CMakeLists.txt properly declares atomspace dependency")

    # Test 2: Verify main CMakeLists.txt declares unify depends on atomspace
    main_cmake = "/home/runner/work/opencog-unified/opencog-unified/CMakeLists.txt"

    with open(main_cmake) as f:
        main_content = f.read()

    assert "add_dependencies(unify atomspace)" in main_content, (
        "Main CMakeLists.txt must declare unify depends on atomspace"
    )
    print("✅ Main CMakeLists.txt properly declares unify dependency on atomspace")

    # Test 3: Verify integration script knows about the dependency
    integration_script = "/home/runner/work/opencog-unified/opencog-unified/integrate-components.sh"

    with open(integration_script) as f:
        integration_content = f.read()

    assert '["unify"]="logic:atomspace"' in integration_content, (
        "Integration script must know unify depends on atomspace"
    )
    print("✅ Integration script properly declares unify dependency on atomspace")

    # Test 4: Check that atomspace directory exists (dependency is satisfied)
    atomspace_dir = "/home/runner/work/opencog-unified/opencog-unified/atomspace"
    assert os.path.exists(atomspace_dir), "AtomSpace dependency must be available"
    print("✅ AtomSpace dependency is satisfied (directory exists)")


if __name__ == "__main__":
    try:
        test_unify_dependency()
        print("SUCCESS: All unify dependency tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
