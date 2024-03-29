from enum import Enum
from typing import Callable

from langchain_core.utils.function_calling import convert_to_openai_tool


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

    def get_definition(self, name: str, **kwargs):
        """
        Return the tool definition.
        """

        for definition in self.definitions:
            if definition["function"]["name"] == name:
                return definition

        raise KeyError(name)

    def get_tool(self, name: str, **kwargs):
        """
        Return the tool callback.
        """

        return self.callbacks[name]

    def list_definitions(self, **kwargs):
        """
        Return the tool definitions.
        """

        return list(self.definitions)

    def list_tools(self, **kwargs):
        """
        Return the tool definitions.
        """

        return list(self.callbacks.keys())


class RuleState(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    SKIP = None


ToolboxRule = tuple[dict[str, str], RuleState]


class RestrictedToolbox(Toolbox):
    """
    Container for tools with restricted access.
    """

    default_state: RuleState
    rules: list[ToolboxRule]

    def __init__(
        self,
        tools: list[Callable],
        rules: list[ToolboxRule],
        default_state=RuleState.DENY,
    ):
        """
        Initialize the toolbox with a list of tools and rules.
        """

        super().__init__(tools)
        self.default_state = default_state
        self.rules = rules

    def check_rule(
        self, rule: ToolboxRule, **kwargs: dict[str, str]
    ) -> RuleState | None:
        """
        Check if the agent has access to the tool.
        """

        criteria, state = rule

        if criteria.items() <= kwargs.items():
            return state

        return None

    def check_rules(self, tool: str, **kwargs):
        """
        Check if the agent has access to the tool.
        """

        kwargs_with_tool = {**kwargs, "tool": tool}
        rule_checks = [self.check_rule(rule, **kwargs_with_tool) for rule in self.rules]

        # filter relevant rules
        relevant_checks = [check for check in rule_checks if check is not None]

        if len(relevant_checks) > 0:
            if any(check for check in relevant_checks if check == RuleState.DENY):
                return RuleState.DENY

            if all(check for check in relevant_checks if check == RuleState.ALLOW):
                return RuleState.ALLOW

        return self.default_state

    def get_definition(self, name: str, **kwargs):
        """
        Return the tool definition.
        """

        if self.check_rules(name, **kwargs) != RuleState.ALLOW:
            raise ValueError(f"Access denied for tool {name}.")

        return super().get_definition(name, **kwargs)

    def get_tool(self, name: str, **kwargs):
        """
        Return the tool callback.
        """

        if self.check_rules(name, **kwargs) != RuleState.ALLOW:
            raise ValueError(f"Access denied for tool {name}.")

        return super().get_tool(name, **kwargs)

    def list_definitions(self, **kwargs):
        return [
            definition
            for definition in super().list_definitions(**kwargs)
            if self.check_rules(definition["function"]["name"], **kwargs)
            == RuleState.ALLOW
        ]

    def list_tools(self, **kwargs):
        """
        Return the tool definitions.
        """

        return [
            name
            for name in super().list_tools(**kwargs)
            if self.check_rules(name, **kwargs) == RuleState.ALLOW
        ]
