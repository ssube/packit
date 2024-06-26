from typing import Literal, Callable
from contextlib import contextmanager

from .console import trace as console_trace
from .spans import SpanKind

TracerIntegrations = Literal["console", "traceloop"]

tracer = console_trace


def set_tracer(fn: Callable | str):
    global tracer

    if isinstance(fn, str):
        if fn == "console":
            from .console import trace as console_trace

            tracer = console_trace
        elif fn == "traceloop":
            # if the user has requested traceloop, import and initialize it
            try:
                from .traceloop import init, trace as traceloop_trace

                init()
                tracer = traceloop_trace
            except ImportError:  # pragma: no cover
                raise ImportError(
                    "To use the traceloop integration, you must install the traceloop-sdk package."
                )
        else:
            raise ValueError(f"Unknown tracer integration name: {fn}")
    elif callable(fn):
        tracer = fn
    else:
        raise ValueError(f"Unknown tracer integration type: {fn}")


@contextmanager
def trace(name: str, kind: str | SpanKind = SpanKind.TASK):
    with tracer(name, kind) as reporters:
        yield reporters
