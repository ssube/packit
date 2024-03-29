"""
Turn math operators into usable tools.
"""


def multiply_tool(a: int, b: int) -> str:
    """Multiply two integers together.

    Args:
        a: First integer
        b: Second integer
    """
    return str(a * b)


def sum_tool(
    a: int, b: int, c: int | None = None, d: int | None = None, e: int | None = None
) -> str:
    """Add two or more integers together.

    Args:
        a: First integer
        b: Second integer
    """
    return str(a + b + (c or 0) + (d or 0) + (e or 0))
