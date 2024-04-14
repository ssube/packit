from enum import Enum


class SpanKind(str, Enum):
    AGENT = "packit.agent"
    EXAMPLE = "packit.example"
    GROUP = "packit.group"
    LOOP = "packit.loop"
    TASK = "packit.task"
    TOOL = "packit.tool"
