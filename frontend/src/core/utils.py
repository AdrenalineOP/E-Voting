"""Utility functions for the application."""
import random
import string


def generate_org_code(length: int = 8) -> str:
    """Generate random organization code with letters and numbers.

    Args:
        length: Code length (max 8, default 8)

    Returns:
        Random code string (e.g., "A3X9K2M1")
    """
    if length > 8:
        length = 8

    # Mix of uppercase letters and digits
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))
