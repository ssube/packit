from json import dumps
from logging import getLogger
from typing import Any

from packit.abac import ABACAttributes
from packit.agent import Agent
from packit.errors import ToolError
from packit.toolbox import Toolbox
from packit.tracing import SpanKind, trace
from packit.types import ResultParser, ToolFilter
from packit.utils import could_be_json, flatten

from .json import json_fixups, json_result
from .primitive import str_result

logger = getLogger(__name__)

FunctionParamsDict = dict[str, Any]
FunctionDict = dict[str, str | FunctionParamsDict]


def function_result(
    value: str,
    abac_context: ABACAttributes | None = None,
    agent: Agent | None = None,
    fix_filter=json_fixups,
    result_parser: ResultParser | None = None,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
    **kwargs,
) -> str:
    # agent and toolbox have to be optional to match the other parser signatures
    if agent is None:
        raise ValueError("Agent is required")

    if toolbox is None:
        raise ValueError("Toolbox is required")

    abac_context = abac_context or {}

    value = value.replace(
        "\\_", "_"
    )  # some models like to escape underscores in the function name

    raw_data = json_result(value, fix_filter=fix_filter)
    normalized_data = normalize_function_json(raw_data)

    if isinstance(normalized_data, list):
        # TODO: should this be allowed without going through one of the multi-function wrappers?
        raise ValueError("Cannot run multiple functions at once")

    if tool_filter is not None:
        filter_result = tool_filter(normalized_data)
        if isinstance(filter_result, str):
            return filter_result

    if "function" not in normalized_data:
        raise ValueError("No function specified")

    function_name = normalized_data["function"]
    if not isinstance(function_name, str):
        raise ValueError("Function name must be a string")

    if function_name not in toolbox.list_tools(abac_context):
        raise ToolError(f"Unknown tool {function_name}", agent, value, function_name)

    logger.debug("Using tool: %s", normalized_data)
    function_params = normalized_data.get("parameters", {})

    tool = toolbox.get_tool(function_name, abac_context)
    try:
        with trace(function_name, SpanKind.TOOL) as (report_args, report_output):
            report_args(**function_params)
            tool_result = tool(**function_params)
            report_output(tool_result)
    except Exception as e:
        raise ToolError(
            f"Error running tool {function_name}: {e}",
            agent,
            value,
            function_name,
        )

    if callable(result_parser):
        tool_result = result_parser(
            tool_result,
            abac_context=abac_context,
            agent=agent,
            fix_filter=fix_filter,
            toolbox=toolbox,
            tool_filter=tool_filter,
        )

    return tool_result


def multi_function_result(
    value: str,
    abac_context: ABACAttributes | None = None,
    agent: Agent | None = None,
    fix_filter=json_fixups,
    result_parser: ResultParser | None = None,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
    **kwargs,
) -> list[str]:
    if fix_filter:
        value = fix_filter(value, list_result=True)

    # split JSON arrays or double line breaks
    if "\n\n" in value:
        calls = value.replace("\r\n", "\n").split("\n\n")
    elif value.startswith("[") and value.endswith("]"):
        json_calls = json_result(
            value.replace("\\_", "_"), list_result=True, fix_filter=None
        )
        calls = [dumps(call) for call in json_calls]
    else:
        calls = [value]

    results = []
    for call in calls:
        try:
            results.append(
                function_result(
                    call,
                    abac_context=abac_context,
                    agent=agent,
                    fix_filter=None,
                    result_parser=result_parser,
                    toolbox=toolbox,
                    tool_filter=tool_filter,
                    **kwargs,
                )
            )
        except Exception as e:
            logger.exception("Error calling tool: %s", call)
            raise e

    return results


def multi_function_or_str_result(
    value: str,
    abac_context: ABACAttributes | None = None,
    agent: Agent | None = None,
    fix_filter=json_fixups,
    result_parser: ResultParser | None = None,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
    **kwargs,
) -> str:
    if could_be_json(value):
        results = multi_function_result(
            value,
            abac_context=abac_context,
            agent=agent,
            fix_filter=fix_filter,
            result_parser=result_parser,
            toolbox=toolbox,
            tool_filter=tool_filter,
            **kwargs,
        )
        return "\n".join([str_result(result) for result in results])

    return str_result(value)


# region json utils


def normalize_function_json(
    data: Any,
) -> FunctionDict | list[FunctionDict]:
    if isinstance(data, list):
        return flatten([normalize_function_json(item) for item in data])

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
