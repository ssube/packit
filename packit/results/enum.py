from typing import List


def enum_result(value: str, enum: List[str] = [], **kwargs) -> str:
    return find_first(value.lower(), [enum_value.lower() for enum_value in enum])


def find_first(haystack: str, needles: List[str]) -> str | None:
    """
    Find the first needle that appears in the haystack.
    """

    needle_idx = [haystack.find(needle) for needle in needles]
    if len([idx for idx in needle_idx if idx != -1]) == 0:
        return None

    # replace missing needles with a value past the end of the haystack
    needle_idx = [idx if idx != -1 else len(haystack) + 1 for idx in needle_idx]

    # find the first needle that appears in the haystack
    first_idx = min([idx for idx in needle_idx if idx != -1])
    return needles[needle_idx.index(first_idx)]
