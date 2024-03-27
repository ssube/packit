from typing import Callable

from langchain_core.utils.function_calling import convert_to_openai_tool


class Toolbox:
    """
    Container for the paired dict and list needed to manage tools.
    """

    callbacks: dict[str, Callable]
    definitions: list[dict]

    def __init__(self, tools: list[Callable]):
        """
        Initialize the toolbox with a list of tools.
        """

        self.callbacks = {}
        self.definitions = []

        for tool in tools:
            name = tool.__name__
            self.callbacks[name] = tool

            self.definitions.append(convert_to_openai_tool(tool))
