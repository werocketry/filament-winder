import math
from typing import Any


def is_object(value: Any) -> bool:
    """
    Check if the given value is an object (not an array, None, or a primitive).
    
    Args:
        value (Any): The value to check.

    Returns:
        bool: True if the value is an object, False otherwise.
    """
    return isinstance(value, dict)


def deg_to_rad(degrees: float) -> float:
    """
    Convert degrees to radians.

    Args:
        degrees (float): The angle in degrees.

    Returns:
        float: The angle in radians.
    """
    return degrees / 180 * math.pi


def rad_to_deg(radians: float) -> float:
    """
    Convert radians to degrees.

    Args:
        radians (float): The angle in radians.

    Returns:
        float: The angle in degrees.
    """
    return radians * 180 / math.pi


def strip_precision(raw_number: float, digits: int = 6) -> float:
    """
    Strip extra precision from a floating-point number.

    Args:
        raw_number (float): The raw floating-point number.
        digits (int, optional): The number of decimal places to keep. Defaults to 6.

    Returns:
        float: The number with reduced precision.
    """
    return round(raw_number, digits)
