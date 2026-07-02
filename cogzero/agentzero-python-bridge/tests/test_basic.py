#!/usr/bin/env python3
"""
Simple test runner for Agent-Zero Python Bridge

Tests basic functionality without requiring full build.
"""

import sys
import os

# Add module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that basic imports work."""
    print("Testing imports...")
    try:
        from opencog.agentzero.exceptions import (
            AgentZeroError,
            AgentZeroRuntimeError,
            AgentZeroConfigError
        )
        print("  ✓ Exception classes imported")
        
        from opencog.agentzero.utils import (
            create_goal,
            create_task,
            format_handle_list
        )
        print("  ✓ Utility functions imported")
        
        # Test creating exceptions
        error = AgentZeroError("Test error")
        assert str(error) == "Test error"
        print("  ✓ Exception creation works")
        
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_exception_hierarchy():
    """Test exception class hierarchy."""
    print("\nTesting exception hierarchy...")
    try:
        from opencog.agentzero.exceptions import (
            AgentZeroError,
            AgentZeroRuntimeError,
            AgentZeroConfigError,
            AgentZeroInitializationError
        )
        
        # Check inheritance
        assert issubclass(AgentZeroRuntimeError, AgentZeroError)
        assert issubclass(AgentZeroConfigError, AgentZeroError)
        assert issubclass(AgentZeroInitializationError, AgentZeroError)
        print("  ✓ Exception hierarchy correct")
        
        # Test raising and catching
        try:
            raise AgentZeroRuntimeError("Test runtime error")
        except AgentZeroError as e:
            assert "Test runtime error" in str(e)
            print("  ✓ Exception catching works")
        
        return True
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False


def test_utility_functions():
    """Test utility functions."""
    print("\nTesting utility functions...")
    try:
        from opencog.agentzero.utils import (
            create_goal,
            create_task,
            format_handle_list
        )
        
        # Test create_goal (stub mode)
        goal = create_goal("TestGoal", "Test description", 0.9)
        assert goal is not None
        print("  ✓ create_goal works")
        
        # Test create_task
        task = create_task("TestTask")
        assert task is not None
        print("  ✓ create_task works")
        
        # Test format_handle_list
        formatted = format_handle_list([])
        assert formatted == "[]"
        print("  ✓ format_handle_list works")
        
        return True
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_stub_classes():
    """Test that stub classes are available when C++ libs not built."""
    print("\nTesting stub implementations...")
    try:
        import warnings
        warnings.simplefilter('ignore')
        
        from opencog.agentzero import (
            AgentZeroCore,
            CognitiveLoop,
            TaskManager,
            KnowledgeIntegrator
        )
        
        print("  ✓ Stub classes available")
        
        # Try to create instances (will use stubs if C++ not available)
        # Check if this is a compiled Cython module by looking for __pyx_vtable__ attribute
        print("  ℹ Cython bindings status:")
        if hasattr(AgentZeroCore, '__pyx_vtable__'):
            print("    - Compiled Cython modules")
        else:
            print("    - Using stub implementations")
        
        return True
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Agent-Zero Python Bridge - Basic Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Exception Hierarchy", test_exception_hierarchy()))
    results.append(("Utility Functions", test_utility_functions()))
    results.append(("Stub Classes", test_stub_classes()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    passed = 0
    failed = 0
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
