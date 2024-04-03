from enum import Enum
from typing import Any, Callable, Protocol, TypeVar

# primitives and type vars
MemoryType = str
PromptType = str
SelectorType = TypeVar("SelectorType")

# ABAC types
ABACAttributes = dict[str, str]


class RuleState(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    SKIP = None


class ABACAdapter(Protocol):
    def check(self, attributes: ABACAttributes) -> RuleState:
        pass  # pragma: no cover


# Loop types
AgentInvoke = Callable[[Any, str, dict], str]
AgentSelector = Callable[[list[SelectorType], int], SelectorType]
MemoryFactory = Callable[[], list[MemoryType]]
MemoryMaker = Callable[[list[MemoryType], MemoryType], None]
PromptTemplate = Callable[[str], PromptType]
PromptFilter = Callable[[PromptType], PromptType | None]
ResultParser = Callable[[PromptType], PromptType]
StopCondition = Callable[
    [int, int], bool
]  # TODO: kwargs and prompts and all those other things
ToolFilter = Callable[[dict], dict | None]
