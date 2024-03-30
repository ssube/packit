from typing import Callable

from langchain_core.utils.function_calling import convert_to_openai_tool

from packit.abac import ABACAdapter, ABACAttributes, RuleState


class Toolbox:
    """
    Container for tools and their metadata.
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

    def get_definition(self, name: str, abac: ABACAttributes = {}):
        """
        Return the tool definition.
        """

        for definition in self.definitions:
            if definition["function"]["name"] == name:
                return definition

        raise KeyError(name)

    def get_tool(self, name: str, abac: ABACAttributes = {}):
        """
        Return the tool callback.
        """

        return self.callbacks[name]

    def list_definitions(self, abac: ABACAttributes = {}):
        """
        Return the tool definitions.
        """

        return list(self.definitions)

    def list_tools(self, abac: ABACAttributes = {}):
        """
        Return the tool definitions.
        """

        return list(self.callbacks.keys())


class RestrictedToolbox(Toolbox):
    """
    Container for tools with restricted access.
    """

    abac: ABACAdapter

    def __init__(
        self,
        tools: list[Callable],
        abac: ABACAdapter,
    ):
        """
        Initialize the toolbox with a list of tools and rules.
        """

        super().__init__(tools)
        self.abac = abac

    def check_tool(self, name: str, abac: ABACAttributes = {}) -> bool:
        """
        Check if the agent has access to the tool.
        """

        return self.abac.check({"resource": name, **abac}) == RuleState.ALLOW

    def get_definition(self, name: str, abac: ABACAttributes = {}):
        """
        Return the tool definition.
        """

        if not self.check_tool(name, abac):
            raise ValueError(f"Access denied for tool {name}.")

        return super().get_definition(name, abac=abac)

    def get_tool(self, name: str, abac: ABACAttributes = {}):
        """
        Return the tool callback.
        """

        if not self.check_tool(name, abac):
            raise ValueError(f"Access denied for tool {name}.")

        return super().get_tool(name, abac=abac)

    def list_definitions(self, abac: ABACAttributes = {}):
        return [
            definition
            for definition in super().list_definitions(abac=abac)
            if self.check_tool(definition["function"]["name"], abac)
        ]

    def list_tools(self, abac: ABACAttributes = {}):
        """
        Return the tool definitions.
        """

        return [
            name
            for name in super().list_tools(abac=abac)
            if self.check_tool(name, abac)
        ]
