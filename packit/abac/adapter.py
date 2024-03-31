from enum import Enum
from typing import Any, Protocol


class RuleState(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    SKIP = None


ABACAttributes = dict[str, str]


class ABACAdapter(Protocol):
    def check(self, attributes: ABACAttributes) -> RuleState:
        pass  # pragma: no cover


GenericRule = tuple[Any, RuleState]
SubsetRule = tuple[dict[str, str], RuleState]


REQUIRED_ATTRIBUTES = ["subject", "resource", "action"]


class SubsetABAC(ABACAdapter):
    default_state: RuleState
    rules: list[SubsetRule]

    def __init__(
        self,
        rules: list[SubsetRule],
        default_state: RuleState = RuleState.DENY,
    ):
        self.rules = rules
        self.default_state = default_state

    def check_rule(
        self,
        rule: SubsetRule,
        attributes: ABACAttributes,
    ) -> RuleState | None:
        """
        Check if the agent has access to the tool.
        """

        criteria, state = rule

        if criteria.items() <= attributes.items():
            return state

        return None

    def check(self, attributes: ABACAttributes) -> RuleState:
        """
        Check if the agent has access to the tool.
        """

        rule_checks = [self.check_rule(rule, attributes) for rule in self.rules]

        # filter relevant rules
        relevant_checks = [check for check in rule_checks if check is not None]

        if len(relevant_checks) > 0:
            if any(check for check in relevant_checks if check == RuleState.DENY):
                return RuleState.DENY

            if all(check for check in relevant_checks if check == RuleState.ALLOW):
                return RuleState.ALLOW

        return self.default_state
