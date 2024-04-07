from json import dumps, loads
from logging import getLogger
from re import sub
from typing import Callable, Literal

from mistletoe import Document
from mistletoe.block_token import CodeFence, Paragraph
from mistletoe.span_token import LineBreak, RawText

from packit.abac import ABACAttributes
from packit.errors import ToolError
from packit.toolbox import Toolbox
from packit.tracing import trace
from packit.types import ResultParser
from packit.utils import could_be_json

logger = getLogger(__name__)


ToolFilter = Callable[[dict], str | None]


def bool_result(value: str, **kwargs) -> bool:
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


def int_result(value: str, **kwargs) -> int:
    value = value.replace("Rating:", "")
    value = value.replace("Rank:", "")
    value = value.strip()

    return int(value)


def str_result(value: str, **kwargs) -> str:
    return str(value).strip()


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


def function_result(
    value: str,
    abac: ABACAttributes = {},
    fix_filter=json_fixups,
    result_parser: ResultParser | None = None,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str:
    value = value.replace(
        "\\_", "_"
    )  # some models like to escape underscores in the function name

    data = json_result(value, fix_filter=fix_filter)
    data = normalize_function_json(data)

    if isinstance(data, list):
        # TODO: should this be allowed without going through one of the multi-function wrappers?
        raise ValueError("Cannot run multiple functions at once")

    if "function" not in data:
        raise ValueError("No function specified")

    function_name = data["function"]
    if function_name not in toolbox.list_tools(abac):
        raise ToolError(f"Unknown tool {function_name}", None, value, function_name)

    logger.debug("Using tool: %s", data)
    function_params = data.get("parameters", {})

    if tool_filter is not None:
        filter_result = tool_filter(data)
        if filter_result is not None:
            return filter_result

    tool = toolbox.get_tool(function_name, abac)
    try:
        with trace(function_name, "packit.tool") as (report_args, report_output):
            report_args(**function_params)
            tool_result = tool(**function_params)
            report_output(tool_result)
    except Exception as e:
        raise ToolError(
            f"Error running tool {function_name}: {e}", None, value, function_name
        )

    if callable(result_parser):
        return result_parser(
            tool_result,
            abac=abac,
            fix_filter=fix_filter,
            toolbox=toolbox,
            tool_filter=tool_filter,
        )

    return tool_result


def multi_function_result(
    value: str,
    abac: ABACAttributes = {},
    fix_filter=json_fixups,
    result_parser: ResultParser | None = None,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> list[str]:
    if fix_filter:
        value = fix_filter(value, list_result=True)

    # split JSON arrays or double line breaks
    if "\n\n" in value:
        calls = value.replace("\r\n", "\n").split("\n\n")
    elif value.startswith("[") and value.endswith("]"):
        calls = json_result(
            value.replace("\\_", "_"), list_result=True, fix_filter=None
        )
        calls = [dumps(call) for call in calls]
    else:
        calls = [value]

    results = []
    for call in calls:
        try:
            results.append(
                function_result(
                    call,
                    abac=abac,
                    fix_filter=None,
                    result_parser=result_parser,
                    toolbox=toolbox,
                    tool_filter=tool_filter,
                )
            )
        except Exception as e:
            logger.exception("Error calling tool: %s", call)
            raise e

    return results


def multi_function_or_str_result(
    value: str,
    toolbox: Toolbox,
    abac: ABACAttributes = {},
    fix_filter=json_fixups,
    result_parser: ResultParser | None = None,
    tool_filter: ToolFilter | None = None,
) -> str:
    if could_be_json(value):
        results = multi_function_result(
            value,
            abac=abac,
            fix_filter=fix_filter,
            result_parser=result_parser,
            toolbox=toolbox,
            tool_filter=tool_filter,
        )
        return "\n".join([str_result(result) for result in results])

    return str_result(value)


MarkdownBlock = Literal["code", "text"]


def markdown_result(
    value: str, block_type: MarkdownBlock = "code", code_language="python"
) -> list[str]:
    """
    Parse a markdown document and return the code blocks or text blocks.

    TODO: replace code_language with a filter function
    """

    def get_paragraph_text(block: Paragraph | RawText) -> str:
        if isinstance(block, RawText):
            return block.content
        if isinstance(block, LineBreak):
            return "\n"

        return "".join([get_paragraph_text(child) for child in block.children])

    document = Document(value)

    if block_type == "code":
        return [
            block.content.strip()
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


def recursive_result(
    result_parser: ResultParser | None = None,
    stop_condition: Callable = lambda *args, **kwargs: False,
):
    def inner(
        value: str,
        abac: ABACAttributes = {},
        fix_filter=json_fixups,
        toolbox: Toolbox | None = None,
        tool_filter: ToolFilter | None = None,
    ) -> str:
        """
        Recursively parse the result, until the stop condition is met.
        """

        result = value

        while not stop_condition(result):
            result = result_parser(
                result,
                abac=abac,
                fix_filter=fix_filter,
                result_parser=result_parser,
                toolbox=toolbox,
                tool_filter=tool_filter,
            )

        return result

    return inner


# region json utils
def normalize_function_json(
    data: dict[str, str] | list[str],
) -> dict[str, str] | list[dict[str, str]]:
    if isinstance(data, list):
        return [normalize_function_json(item) for item in data]

    if "function" in data and isinstance(data["function"], dict):
        if "parameters" in data["function"]:
            return {
                "function": data["function"]["name"],
                "parameters": data["function"]["parameters"],
            }
        else:
            return {
                "function": data["function"]["name"],
                "parameters": data.get("parameters", {}),
            }
    elif "function" in data and isinstance(data["function"], str):
        return {
            "function": data["function"],
            "parameters": data.get("parameters", {}),
        }
    else:
        return data


# endregion
