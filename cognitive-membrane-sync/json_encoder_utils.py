#!/usr/bin/env python3
"""
JSON Encoder Utilities for Cognitive Membrane Sync
Handles serialization of NumPy types and other non-JSON-serializable objects
"""

import json
from typing import Any

import numpy as np


class EnhancedJSONEncoder(json.JSONEncoder):
    """
    Enhanced JSON encoder that handles NumPy types and other special types.

    Supports:
    - NumPy integers (int8, int16, int32, int64, uint8, uint16, uint32, uint64)
    - NumPy floats (float16, float32, float64)
    - NumPy booleans
    - NumPy arrays (converted to lists)
    - Other NumPy generic types
    """

    def default(self, obj: Any) -> Any:
        """
        Override default method to handle NumPy types.

        Args:
            obj: Object to serialize

        Returns:
            JSON-serializable representation of the object

        Raises:
            TypeError: If object type is not supported
        """
        # Handle NumPy integers (NumPy 2.0 compatible)
        if isinstance(obj, (np.integer, np.intc, np.intp, np.int8,
                           np.int16, np.int32, np.int64,
                           np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)

        # Handle NumPy floats (NumPy 2.0 compatible)
        if isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
            return float(obj)

        # Handle NumPy booleans
        if isinstance(obj, (np.bool_, bool)):
            return bool(obj)

        # Handle NumPy arrays
        if isinstance(obj, np.ndarray):
            return obj.tolist()

        # Handle NumPy generic types
        if isinstance(obj, np.generic):
            return obj.item()

        # Fallback to default encoder
        return super().default(obj)


def deep_convert(obj: Any) -> Any:
    """
    Recursively convert NumPy types to native Python types in nested structures.

    This function is useful for deeply nested dictionaries and lists that may
    contain NumPy types at any level.

    Args:
        obj: Object to convert (can be dict, list, or any other type)

    Returns:
        Object with all NumPy types converted to native Python types
    """
    if isinstance(obj, dict):
        return {k: deep_convert(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [deep_convert(item) for item in obj]

    # Handle NumPy integers (NumPy 2.0 compatible)
    if isinstance(obj, (np.integer, np.intc, np.intp, np.int8,
                       np.int16, np.int32, np.int64,
                       np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)

    # Handle NumPy floats (NumPy 2.0 compatible)
    if isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
        return float(obj)

    # Handle NumPy booleans
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)

    # Handle NumPy arrays
    if isinstance(obj, np.ndarray):
        return obj.tolist()

    # Handle NumPy generic types
    if isinstance(obj, np.generic):
        return obj.item()

    # Return as-is for other types
    return obj


def safe_json_dump(obj: Any, fp, **kwargs) -> None:
    """
    Safely dump object to JSON file with NumPy type handling.

    Args:
        obj: Object to serialize
        fp: File pointer to write to
        **kwargs: Additional arguments to pass to json.dump
    """
    # Ensure 'cls' parameter is set to our enhanced encoder if not provided
    if 'cls' not in kwargs:
        kwargs['cls'] = EnhancedJSONEncoder

    json.dump(obj, fp, **kwargs)


def safe_json_dumps(obj: Any, **kwargs) -> str:
    """
    Safely serialize object to JSON string with NumPy type handling.

    Args:
        obj: Object to serialize
        **kwargs: Additional arguments to pass to json.dumps

    Returns:
        JSON string representation
    """
    # Ensure 'cls' parameter is set to our enhanced encoder if not provided
    if 'cls' not in kwargs:
        kwargs['cls'] = EnhancedJSONEncoder

    return json.dumps(obj, **kwargs)


# Convenience function for the default encoder callback style
def enhanced_json_encoder(obj: Any) -> Any:
    """
    Enhanced JSON encoder function for use with json.dump(s) default parameter.

    Usage:
        json.dumps(data, default=enhanced_json_encoder)

    Args:
        obj: Object to serialize

    Returns:
        JSON-serializable representation

    Raises:
        TypeError: If object type is not supported
    """
    # Handle NumPy integers (NumPy 2.0 compatible)
    if isinstance(obj, (np.integer, np.intc, np.intp, np.int8,
                       np.int16, np.int32, np.int64,
                       np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)

    # Handle NumPy floats (NumPy 2.0 compatible)
    if isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
        return float(obj)

    # Handle NumPy booleans
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)

    # Handle NumPy arrays
    if isinstance(obj, np.ndarray):
        return obj.tolist()

    # Handle NumPy generic types
    if isinstance(obj, np.generic):
        return obj.item()

    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
