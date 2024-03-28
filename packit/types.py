from typing import Callable, TypeVar

MemoryType = str
PromptType = str
SelectorType = TypeVar("SelectorType")

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
