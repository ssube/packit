from typing import Callable

MemoryFactory = Callable[[], list[str]]
MemoryMaker = Callable[[list[str], str], None]
PromptTemplate = Callable[[str], str]
ResultParser = Callable[[str], str]
StopCondition = Callable[
    [int, int], bool
]  # TODO: kwargs and prompts and all those other things
ToolFilter = Callable[[dict], bool]
