from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# primitives and type vars
MemoryType = str | AIMessage | HumanMessage | SystemMessage
PromptType = str
SelectorType = TypeVar("SelectorType")

# ABAC types
ABACAttributes = Dict[str, str]


class RuleState(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    SKIP = None


class ABACAdapter(Protocol):
    def check(self, attributes: ABACAttributes) -> RuleState:
        pass  # pragma: no cover


class AgentInvoker(Protocol):
    def __call__(
        self,
        agent: Any,
        prompt: PromptType,
        context: "AgentContext",
        memory: List[MemoryType] | None = None,
        prompt_template: Optional["PromptTemplate"] = None,
        toolbox: Any | None = None,
    ) -> PromptType:
        pass  # pragma: no cover


class ResultParser(Protocol):
    def __call__(
        self,
        value: PromptType,
        # abac_context: ABACAttributes | None = None,
        # fix_filter: Callable | None = None,
        # result_parser: Optional["ResultParser"] = None,
        # toolbox: Any | None = None,
        # tool_filter: Optional["ToolFilter"] = None,
        **kwargs,
    ) -> Any:
        pass


class StopCondition(Protocol):
    # TODO: kwargs and prompts and all those other things
    def __call__(self, max: int, current: int) -> bool:
        pass  # pragma: no cover


# Loop types
AgentContext = Dict[str, str | List[str]]
AgentSelector = Callable[[list[SelectorType], int], SelectorType]
MemoryFactory = Callable[[], list[MemoryType]]
MemoryMaker = Callable[[list[MemoryType], MemoryType], None]
PromptTemplate = Callable[[str], PromptType]
PromptFilter = Callable[[PromptType], PromptType | None]
ToolFilter = Callable[[dict], dict | str | None]
