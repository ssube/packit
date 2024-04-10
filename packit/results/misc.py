from logging import getLogger
from typing import Callable

from packit.abac import ABACAttributes
from packit.toolbox import Toolbox
from packit.types import ResultParser, ToolFilter

from .json import json_fixups

logger = getLogger(__name__)


def recursive_result(
    result_parser: ResultParser,
    stop_condition: Callable = lambda *args, **kwargs: False,
):
    outer_result_parser = result_parser

    def inner(
        value: str,
        abac_context: ABACAttributes = {},
        fix_filter=json_fixups,
        result_parser: ResultParser | None = None,
        toolbox: Toolbox | None = None,
        tool_filter: ToolFilter | None = None,
    ) -> str:
        """
        Recursively parse the result, until the stop condition is met.
        """

        result = value

        while not stop_condition(result):
            result = outer_result_parser(
                result,
                abac_context=abac_context,
                fix_filter=fix_filter,
                result_parser=outer_result_parser,
                toolbox=toolbox,
                tool_filter=tool_filter,
            )

        return result

    return inner
