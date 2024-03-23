"""
Turn str methods into usable tools.
"""


def lowercase_tool(a: str) -> str:
    """
    Lowercase a string.

    Args:
        a: The string to lowercase.
    """
    return a.lower()


def uppercase_tool(a: str) -> str:
    """
    Uppercase a string.

    Args:
        a: The string to uppercase.
    """
    return a.upper()


def titlecase_tool(a: str) -> str:
    """
    Titlecase a string.

    Args:
        a: The string to titlecase.
    """
    return a.title()
