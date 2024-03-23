"""
Turn math operators into usable tools.
"""


def multiply_tool(a: int, b: int) -> int:
    """Multiply two integers together.

    Args:
        a: First integer
        b: Second integer
    """
    return a * b


def sum_tool(a: int, b: int, c: int = None, d: int = None, e: int = None) -> int:
    """Add two or more integers together.

    Args:
        a: First integer
        b: Second integer
    """
    return a + b + (c or 0) + (d or 0) + (e or 0)
