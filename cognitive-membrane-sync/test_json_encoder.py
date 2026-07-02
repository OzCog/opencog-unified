#!/usr/bin/env python3
"""
Test suite for JSON encoder utilities
Validates that NumPy types are properly handled during JSON serialization
"""

import json
import sys
from pathlib import Path


# Add cognitive-membrane-sync to path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
from json_encoder_utils import deep_convert, enhanced_json_encoder, safe_json_dump, safe_json_dumps


def test_numpy_integers():
    """Test serialization of NumPy integer types"""
    print("Testing NumPy integers...")

    test_data = {
        'int8': np.int8(42),
        'int16': np.int16(1000),
        'int32': np.int32(100000),
        'int64': np.int64(10000000000),
        'uint8': np.uint8(255),
        'uint16': np.uint16(65535),
        'uint32': np.uint32(4294967295),
        'uint64': np.uint64(18446744073709551615)
    }

    # Test with safe_json_dumps
    json_str = safe_json_dumps(test_data)
    reloaded = json.loads(json_str)

    assert reloaded['int64'] == 10000000000, "int64 not properly converted"
    assert isinstance(reloaded['int64'], int), "int64 not converted to Python int"

    print("✅ NumPy integers test passed")


def test_numpy_floats():
    """Test serialization of NumPy float types"""
    print("Testing NumPy floats...")

    test_data = {
        'float16': np.float16(3.14),
        'float32': np.float32(2.71828),
        'float64': np.float64(1.41421356)
    }

    # Test with safe_json_dumps
    json_str = safe_json_dumps(test_data)
    reloaded = json.loads(json_str)

    assert isinstance(reloaded['float64'], float), "float64 not converted to Python float"

    print("✅ NumPy floats test passed")


def test_numpy_arrays():
    """Test serialization of NumPy arrays"""
    print("Testing NumPy arrays...")

    test_data = {
        'array_1d': np.array([1, 2, 3, 4, 5]),
        'array_2d': np.array([[1, 2], [3, 4]]),
        'array_3d': np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    }

    # Test with safe_json_dumps
    json_str = safe_json_dumps(test_data)
    reloaded = json.loads(json_str)

    assert reloaded['array_1d'] == [1, 2, 3, 4, 5], "1D array not properly converted"
    assert reloaded['array_2d'] == [[1, 2], [3, 4]], "2D array not properly converted"
    assert isinstance(reloaded['array_1d'], list), "Array not converted to list"

    print("✅ NumPy arrays test passed")


def test_numpy_boolean():
    """Test serialization of NumPy boolean types"""
    print("Testing NumPy booleans...")

    test_data = {
        'bool_true': np.bool_(True),
        'bool_false': np.bool_(False)
    }

    # Test with safe_json_dumps
    json_str = safe_json_dumps(test_data)
    reloaded = json.loads(json_str)

    assert reloaded['bool_true'] is True, "bool_ True not properly converted"
    assert reloaded['bool_false'] is False, "bool_ False not properly converted"
    assert isinstance(reloaded['bool_true'], bool), "bool_ not converted to Python bool"

    print("✅ NumPy booleans test passed")


def test_nested_structures():
    """Test serialization of nested structures with NumPy types"""
    print("Testing nested structures...")

    test_data = {
        'organizations': {
            'cogpilot': {
                'prime': np.int64(2),
                'repositories': [
                    {
                        'complexity': np.float64(4.5),
                        'shape': np.array([3, 3, 2])
                    }
                ]
            },
            'OzCog': {
                'prime': np.int64(3),
                'tensor_shape': [np.int32(7), np.int32(2), np.int32(1)]
            }
        },
        'tensor_dimensions': [np.int64(7), np.int64(3), np.int64(10), np.int64(50), np.int64(100)]
    }

    # Test with safe_json_dumps
    json_str = safe_json_dumps(test_data)
    reloaded = json.loads(json_str)

    assert reloaded['organizations']['cogpilot']['prime'] == 2, "Nested int64 not converted"
    assert reloaded['organizations']['cogpilot']['repositories'][0]['shape'] == [3, 3, 2], "Nested array not converted"
    assert reloaded['tensor_dimensions'] == [7, 3, 10, 50, 100], "List of int64 not converted"

    print("✅ Nested structures test passed")


def test_deep_convert():
    """Test deep_convert function"""
    print("Testing deep_convert...")

    test_data = {
        'level1': {
            'level2': {
                'level3': {
                    'value': np.int64(42),
                    'array': np.array([1, 2, 3])
                }
            }
        }
    }

    converted = deep_convert(test_data)

    # Verify types are converted
    assert isinstance(converted['level1']['level2']['level3']['value'], int)
    assert isinstance(converted['level1']['level2']['level3']['array'], list)

    # Should be serializable with standard json
    json_str = json.dumps(converted)
    reloaded = json.loads(json_str)

    assert reloaded['level1']['level2']['level3']['value'] == 42

    print("✅ deep_convert test passed")


def test_enhanced_json_encoder_callback():
    """Test enhanced_json_encoder callback function"""
    print("Testing enhanced_json_encoder callback...")

    test_data = {
        'value': np.int64(123),
        'array': np.array([1, 2, 3])
    }

    # Use with standard json.dumps and default parameter
    json_str = json.dumps(test_data, default=enhanced_json_encoder)
    reloaded = json.loads(json_str)

    assert reloaded['value'] == 123
    assert reloaded['array'] == [1, 2, 3]

    print("✅ enhanced_json_encoder callback test passed")


def test_file_operations():
    """Test safe_json_dump with file operations"""
    print("Testing file operations...")

    test_data = {
        'enterprise': 'test',
        'complexity': np.float64(10.5),
        'tensor_shape': np.array([7, 3, 10])
    }

    test_file = Path('/tmp/test_json_encoder.json')

    # Write to file
    with open(test_file, 'w') as f:
        safe_json_dump(test_data, f, indent=2)

    # Read and verify
    with open(test_file) as f:
        reloaded = json.load(f)

    assert reloaded['complexity'] == 10.5
    assert reloaded['tensor_shape'] == [7, 3, 10]

    # Cleanup
    test_file.unlink()

    print("✅ File operations test passed")


def test_numpy_prod_conversion():
    """Test that np.prod results are properly handled"""
    print("Testing np.prod conversion...")

    shape = np.array([3, 3, 3])
    test_data = {
        'shape': shape,
        'degrees_of_freedom': np.prod(shape)  # Returns np.int64
    }

    # Should work with safe_json_dumps
    json_str = safe_json_dumps(test_data)
    reloaded = json.loads(json_str)

    assert reloaded['degrees_of_freedom'] == 27
    assert isinstance(reloaded['degrees_of_freedom'], int)

    print("✅ np.prod conversion test passed")


def run_all_tests():
    """Run all test cases"""
    print("=" * 60)
    print("Running JSON Encoder Utility Test Suite")
    print("=" * 60)
    print()

    tests = [
        test_numpy_integers,
        test_numpy_floats,
        test_numpy_arrays,
        test_numpy_boolean,
        test_nested_structures,
        test_deep_convert,
        test_enhanced_json_encoder_callback,
        test_file_operations,
        test_numpy_prod_conversion
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()

    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
