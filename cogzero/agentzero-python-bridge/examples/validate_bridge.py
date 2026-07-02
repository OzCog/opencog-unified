#!/usr/bin/env python3
"""
Validation Example for Agent-Zero Python Bridge

This example validates the Python bridge structure without requiring
the full OpenCog stack to be built.
"""

import sys
import os

# Add module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Validate the Python bridge."""
    print("=" * 60)
    print("Agent-Zero Python Bridge - Validation")
    print("=" * 60)
    
    # Test 1: Import exceptions
    print("\n1. Testing exception classes...")
    try:
        from opencog.agentzero.exceptions import (
            AgentZeroError,
            AgentZeroRuntimeError,
            AgentZeroConfigError,
            AgentZeroInitializationError,
            AgentZeroTaskError,
            AgentZeroKnowledgeError
        )
        print("   ✓ All exception classes imported successfully")
    except ImportError as e:
        print(f"   ✗ Failed to import exceptions: {e}")
        return 1
    
    # Test 2: Import utilities
    print("\n2. Testing utility functions...")
    try:
        from opencog.agentzero.utils import (
            create_goal,
            create_task,
            query_knowledge,
            format_handle_list,
            create_action,
            get_agent_statistics
        )
        print("   ✓ All utility functions imported successfully")
        
        # Test utility functions
        goal = create_goal("TestGoal", "Test description", 0.9)
        print(f"   ✓ Created goal: {goal}")
        
        task = create_task("TestTask")
        print(f"   ✓ Created task: {task}")
        
    except ImportError as e:
        print(f"   ✗ Failed to import utilities: {e}")
        return 1
    
    # Test 3: Import core bindings (stub mode)
    print("\n3. Testing core bindings...")
    try:
        import warnings
        warnings.simplefilter('ignore')
        
        from opencog.agentzero import (
            AgentZeroCore,
            CognitiveLoop,
            TaskManager,
            KnowledgeIntegrator
        )
        print("   ✓ Core binding classes available")
        print("   ℹ Note: Using stub implementations (C++ libraries not built)")
        
    except ImportError as e:
        print(f"   ✗ Failed to import core bindings: {e}")
        return 1
    
    # Test 4: Test exception handling
    print("\n4. Testing exception handling...")
    try:
        raise AgentZeroRuntimeError("Test error")
    except AgentZeroError as e:
        print(f"   ✓ Exception handling works: caught '{e}'")
    except Exception as e:
        print(f"   ✗ Unexpected exception: {e}")
        return 1
    
    # Test 5: Module metadata
    print("\n5. Checking module metadata...")
    try:
        import opencog.agentzero as az
        print(f"   ✓ Version: {az.__version__}")
        print(f"   ✓ Available exports: {len(az.__all__)} items")
        print(f"   ✓ Module ready for integration")
    except Exception as e:
        print(f"   ✗ Failed to check metadata: {e}")
        return 1
    
    # Summary
    print("\n" + "=" * 60)
    print("Validation Results")
    print("=" * 60)
    print("✓ All validation tests passed!")
    print("\nNext steps:")
    print("  1. Build cogutil and atomspace C++ libraries")
    print("  2. Build agentzero-core C++ library")
    print("  3. Build Python bindings with: cmake .. && make")
    print("  4. Install with: sudo make install")
    print("  5. Test with full OpenCog integration")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
