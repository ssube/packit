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

    try:
        if match:
            return float(match.group())

        raise ValueError(
            f"No decimal number found in {value}. Please provide a number."
        )
    except ValueError:
        raise ValueError(f"{value} is not a valid decimal number.")


def int_result(value: str, **kwargs) -> int:
    value = remove_prefix(value)

    try:
        return int(value)
    except ValueError:
        raise ValueError(f"No integer found in {value}. Please provide an integer.")


def str_result(value: str, **kwargs) -> str:
    return str(value).strip()
