from json import loads
from logging import getLogger
from re import sub
from typing import Callable

logger = getLogger(__name__)


def bool_result(value: str) -> bool:
    value = value.replace("Rating:", "")
    value = value.replace("Rank:", "")
    value = value.strip()

    # take the first phrase from longer answers
    if "," in value:
        value = value.split(",")[0]

    # take the first word from longer answers
    if " " in value:
        value = value.split(" ")[0]

    return value.lower() == "yes"


def int_result(value: str) -> int:
    value = value.replace("Rating:", "")
    value = value.replace("Rank:", "")
    value = value.strip()

    return int(value)


def json_result(value: str, list_result=False) -> list[str] | dict[str, str]:
    # collapse lines
    value = value.replace("\n", "").replace("\r", "")

    value = sub(
        r"<\/\|.*$", "", value
    )  # sometimes the system prompt leaks into the output, like <|assistant|>
    value = sub(
        r"^[\s\w\.,:]+ \[", "", value
    )  # sometimes the output will have a leading comment, like "This is the list: []"
    value = value.replace('""', '"')  # the robots will double some JSON quotes

    # if they forgot to close the array, fix that
    if list_result and value.endswith('"}'):
        value = value + "]"

    # if they forgot to open the array and left it out entirely, fix that
    if list_result and value.startswith('{"'):
        value = "[" + value

    # remove leading/trailing whitespace
    value = value.strip()

    logger.debug("JSON after fixups: %s", value)
    return loads(value)


ToolDict = dict[str, Callable | tuple[Callable, Callable | None]]


def function_result(value: str, tools: ToolDict) -> str:
    value = value.replace(
        "\\_", "_"
    )  # some models like to escape underscores in the function name
    value = value.replace("<|im_end|>", "")  # some models include this terminator
    data = json_result(value)

    if "function" not in data:
        raise ValueError("No function specified")

    function_name = data["function"]
    if function_name not in tools:
        raise ValueError(f"Unknown tool {function_name}")

    function_params = data.get("parameters", {})
    tool_function, result_parser = get_tool_with_parser(tools[function_name])

    try:
        tool_result = tool_function(**function_params)
    except Exception as e:
        raise ValueError(f"Error running tool {function_name}: {e}")

    if result_parser is None:
        return tool_result

    return result_parser(tool_result)


def get_tool_with_parser(
    tool: Callable | tuple[Callable, Callable | None]
) -> tuple[Callable, Callable | None]:
    if isinstance(tool, tuple):
        return tool

    return tool, None
