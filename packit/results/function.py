from json import dumps
from logging import getLogger
from typing import Any

from packit.abac import ABACAttributes
from packit.errors import ToolError
from packit.toolbox import Toolbox
from packit.tracing import trace
from packit.types import ResultParser, ToolFilter
from packit.utils import could_be_json

from .json import json_fixups, json_result
from .primitive import str_result

logger = getLogger(__name__)

FunctionParamsDict = dict[str, Any]
FunctionDict = dict[str, str | FunctionParamsDict]


def function_result(
    value: str,
    abac_context: ABACAttributes | None = None,
    fix_filter=json_fixups,
    result_parser: ResultParser | None = None,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str:
    # toolbox has to be optional to match the other parser signatures
    if toolbox is None:
        raise ValueError("Toolbox is required")

    abac_context = abac_context or {}

    value = value.replace(
        "\\_", "_"
    )  # some models like to escape underscores in the function name

    data = json_result(value, fix_filter=fix_filter)
    data = normalize_function_json(data)

    if isinstance(data, list):
        # TODO: should this be allowed without going through one of the multi-function wrappers?
        raise ValueError("Cannot run multiple functions at once")

    if tool_filter is not None:
        filter_result = tool_filter(data)
        if filter_result is not None:
            return filter_result

    if "function" not in data:
        raise ValueError("No function specified")

    function_name = data["function"]
    if function_name not in toolbox.list_tools(abac_context):
        raise ToolError(f"Unknown tool {function_name}", None, value, function_name)

    logger.debug("Using tool: %s", data)
    function_params: FunctionParamsDict = data.get("parameters", {})

    tool = toolbox.get_tool(function_name, abac_context)
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
        tool_result = result_parser(
            tool_result,
            abac_context=abac_context,
            fix_filter=fix_filter,
            toolbox=toolbox,
            tool_filter=tool_filter,
        )

    return tool_result


def multi_function_result(
    value: str,
    abac_context: ABACAttributes | None = None,
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
                    abac_context=abac_context,
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
    abac_context: ABACAttributes | None = None,
    fix_filter=json_fixups,
    result_parser: ResultParser | None = None,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str:
    if could_be_json(value):
        results = multi_function_result(
            value,
            abac_context=abac_context,
            fix_filter=fix_filter,
            result_parser=result_parser,
            toolbox=toolbox,
            tool_filter=tool_filter,
        )
        return "\n".join([str_result(result) for result in results])

    return str_result(value)


# region json utils


def normalize_function_json(
    data: Any,
) -> FunctionDict | list[FunctionDict]:
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
