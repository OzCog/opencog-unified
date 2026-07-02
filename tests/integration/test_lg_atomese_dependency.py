#!/usr/bin/env python3
"""
Integration test for lg-atomese atomspace dependency
"""

import os
import sys


def test_lg_atomese_dependency():
    """Test that lg-atomese properly requires atomspace"""

    # Test 1: Verify lg-atomese CMakeLists.txt declares atomspace dependency
    cmake_file = "/home/runner/work/opencog-unified/opencog-unified/lg-atomese/CMakeLists.txt"

    with open(cmake_file) as f:
        content = f.read()

    assert "find_package(AtomSpace" in content, "lg-atomese must declare AtomSpace dependency"
    assert "CONFIG REQUIRED" in content, "lg-atomese must require AtomSpace with CONFIG REQUIRED"
    assert "HAVE_ATOMSPACE" in content, "lg-atomese must check for HAVE_ATOMSPACE"
    print("✅ lg-atomese CMakeLists.txt properly declares atomspace dependency")

    # Test 2: Verify main CMakeLists.txt declares lg-atomese depends on atomspace
    main_cmake = "/home/runner/work/opencog-unified/opencog-unified/CMakeLists.txt"

    with open(main_cmake) as f:
        main_content = f.read()

    assert "add_dependencies(lg-atomese atomspace)" in main_content, (
        "Main CMakeLists.txt must declare lg-atomese depends on atomspace"
    )
    print("✅ Main CMakeLists.txt properly declares lg-atomese dependency on atomspace")

    # Test 3: Verify integration script knows about the dependency
    integration_script = "/home/runner/work/opencog-unified/opencog-unified/integrate-components.sh"

    with open(integration_script) as f:
        integration_content = f.read()

    assert '"lg-atomese"]="language:atomspace"' in integration_content, (
        "Integration script must know lg-atomese depends on atomspace"
    )
    print("✅ Integration script properly declares lg-atomese dependency on atomspace")

    # Test 4: Check that atomspace directory exists (dependency is satisfied)
    atomspace_dir = "/home/runner/work/opencog-unified/opencog-unified/atomspace"
    assert os.path.exists(atomspace_dir), "AtomSpace dependency must be present"
    assert os.path.exists(os.path.join(atomspace_dir, "CMakeLists.txt")), "AtomSpace must have CMakeLists.txt"
    print("✅ AtomSpace dependency is satisfied (directory exists)")

    print("\n🎉 All lg-atomese dependency integration tests passed!")
    print("✅ lg-atomese properly requires atomspace as specified in the issue")

    return True


if __name__ == "__main__":
    try:
        test_lg_atomese_dependency()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
