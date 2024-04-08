from json import loads
from logging import getLogger
from re import sub

logger = getLogger(__name__)


def json_fixups(value: str, list_result=False, **kwargs) -> str:
    value = value.strip()

    # collapse lines
    value = value.replace("\n", "").replace("\r", "")

    value = sub(
        r"<\/\|.*$", "", value
    )  # sometimes the system prompt leaks into the output, like <|assistant|>
    value = sub(
        r"^[\s\w\.,:]+ \[", "", value
    )  # sometimes the output will have a leading comment, like "This is the list: []"
    value = value.replace('""', '"')  # the robots will double some JSON quotes
    value = value.replace(
        "}{", "},{"
    )  # the robots will sometimes forget commas between objects

    # if they forgot to open the array and left it out entirely, fix that
    if list_result and value.startswith('{"'):
        value = "[" + value

    # if they forgot to close the array, fix that
    # this is complicated by the fact that the ending may have multiple closing braces
    if list_result and value.startswith("[") and value.endswith("}"):
        value = value + "]"

    # remove leading/trailing whitespace
    value = value.strip()

    logger.debug("JSON after fixups: %s", value)
    return value


def json_result(
    value: str, list_result=False, fix_filter=json_fixups, *kwargs
) -> list[str] | dict[str, str]:
    if callable(fix_filter):
        value = fix_filter(value, list_result=list_result)

    return loads(value)
