import re

REMOVE_PREFIXES = [
    "Rating:",
    "Rank:",
]


def remove_prefix(value: str, **kwargs) -> str:
    for prefix in REMOVE_PREFIXES:
        value = value.replace(prefix, "")

    return value.strip()


def bool_result(value: str, **kwargs) -> bool:
    value = remove_prefix(value)

    # take the first phrase from longer answers
    if "." in value:
        value = value.split(".")[0]

    if "," in value:
        value = value.split(",")[0]

    # take the first word from longer answers
    if " " in value:
        value = value.split(" ")[0]

    return value.lower() == "yes"


def float_result(value: str, **kwargs) -> float:
    """
    Parses the first floating point number found in the input value.

    Parameters:
    value (str): The string containing the potential floating point number.

    Returns:
    float: The first floating point number found, or None if no number is found.
    """
    value = remove_prefix(value)

    pattern = re.compile(r"[-+]?\d*\.?\d+")
    match = pattern.search(value)

    if match:
        return float(match.group())

    raise ValueError(f"No floating point number found in {value}")


def int_result(value: str, **kwargs) -> int:
    value = remove_prefix(value)

    return int(value)


def str_result(value: str, **kwargs) -> str:
    return str(value).strip()
