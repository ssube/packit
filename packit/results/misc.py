from logging import getLogger
from typing import Callable

from packit.abac import ABACAttributes
from packit.toolbox import Toolbox
from packit.types import ResultParser, ToolFilter

from .json import json_fixups

logger = getLogger(__name__)


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
