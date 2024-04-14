from logging import getLogger
from typing import Callable

from packit.types import ResultParser

logger = getLogger(__name__)


def recursive_result(
    result_parser: ResultParser,
    stop_condition: Callable = lambda *args, **kwargs: False,
):
    outer_result_parser = result_parser

    def inner(
        value: str,
        **kwargs,
    ) -> str:
        """
        Recursively parse the result, until the stop condition is met.
        """

        result = value

        while not stop_condition(result):
            result = outer_result_parser(
                result,
                **kwargs,
            )

        return result

    return inner
