from json import loads
from logging import getLogger
from re import sub
from typing import Callable, Literal

from packit.utils import could_be_json

logger = getLogger(__name__)


def bool_result(value: str) -> bool:
    value = value.replace("Rating:", "")
    value = value.replace("Rank:", "")
    value = value.strip()

    # take the first phrase from longer answers
    if "." in value:
        value = value.split(".")[0]

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


def str_result(value: str) -> str:
    return str(value).strip()


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


ToolFilter = Callable[[dict], str | None]
ToolDict = dict[str, Callable | tuple[Callable, Callable | None]]


def function_result(
    value: str, tools: ToolDict, tool_filter: ToolFilter | None = None
) -> str:
    value = value.replace(
        "\\_", "_"
    )  # some models like to escape underscores in the function name
    value = value.replace("<|im_end|>", "")  # some models include this terminator

    data = json_result(value)
    data = normalize_function_json(data)

    if "function" not in data:
        raise ValueError("No function specified")

    function_name = data["function"]
    if function_name not in tools:
        raise ValueError(f"Unknown tool {function_name}")

    function_params = data.get("parameters", {})
    tool_function, result_parser = get_tool_with_parser(tools[function_name])

    if tool_filter is not None:
        filter_result = tool_filter(data)
        if filter_result is not None:
            return filter_result

    try:
        tool_result = tool_function(**function_params)
    except Exception as e:
        raise ValueError(f"Error running tool {function_name}: {e}")

    if result_parser is None:
        return tool_result

    return result_parser(tool_result)


def multi_function_result(
    value: str, tools: ToolDict, tool_filter: ToolFilter | None = None
) -> list[str]:
    calls = value.replace("\r\n", "\n").split("\n\n")
    results = []
    for call in calls:
        try:
            results.append(function_result(call, tools, tool_filter=tool_filter))
        except Exception as e:
            logger.error("Error calling function: %s", e)
            results.append(f"Error: {e}")

    return results


def multi_function_or_str_result(
    value: str, tools: ToolDict, tool_filter: ToolFilter | None = None
) -> str:
    try:
        if could_be_json(value):
            return multi_function_result(value, tools, tool_filter=tool_filter)

        return [str_result(value)]
    except Exception as e:
        logger.error("Error calling function: %s", e)
        return [f"Error: {e}"]


MarkdownBlock = Literal["code", "text"]


def markdown_result(
    value: str, block_type: MarkdownBlock = "code", code_language="python"
) -> str:
    """
    Parse a markdown document and return the code blocks or text blocks.

    TODO: replace code_language with a filter function
    """
    from mistletoe import Document
    from mistletoe.block_token import CodeFence, Paragraph
    from mistletoe.span_token import RawText

    def get_paragraph_text(block: Paragraph | RawText) -> str:
        if isinstance(block, RawText):
            return block.content

        return "".join([get_paragraph_text(child) for child in block.children])

    document = Document(value)

    if block_type == "code":
        return [
            block.content
            for block in document.children
            if isinstance(block, CodeFence) and block.info_string == code_language
        ]
    elif block_type == "text":
        return [
            get_paragraph_text(block)
            for block in document.children
            if isinstance(block, (Paragraph, RawText))
        ]
    else:
        raise ValueError("Invalid block type")


# region internal utils
def get_tool_with_parser(
    tool: Callable | tuple[Callable, Callable | None]
) -> tuple[Callable, Callable | None]:
    if isinstance(tool, tuple):
        return tool

    return tool, None


def normalize_function_json(
    data: dict,
) -> dict:
    if "function" in data and isinstance(data["function"], dict):
        return {
            "function": data["function"]["name"],
            "parameters": data["function"].get("parameters", {}),
        }
    elif "function" in data and isinstance(data["function"], str):
        return {
            "function": data["function"],
            "parameters": data.get("parameters", {}),
        }
    else:
        return data


# endregion
