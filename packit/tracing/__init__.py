from typing import Literal, Callable
from contextlib import contextmanager

from .console import trace

TracerIntegrations = Literal["console", "traceloop"]

tracer = trace


def set_tracer(fn: Callable | str):
    global tracer

    if isinstance(fn, str):
        if fn == "console":
            from .console import trace

            tracer = trace
        elif fn == "traceloop":
            from .traceloop import trace

            # if the user has requested traceloop, import and initialize it
            try:
                from traceloop.sdk import Traceloop

                Traceloop.init(disable_batch=True)
            except ImportError:
                raise ImportError(
                    "To use the traceloop integration, you must install the traceloop SDK."
                )

            tracer = trace
        else:
            raise ValueError(f"Unknown tracer integration name: {fn}")
    elif callable(fn):
        tracer = fn
    else:
        raise ValueError(f"Unknown tracer integration type: {fn}")


@contextmanager
def trace(name: str, kind: str = "task"):
    with tracer(name, kind) as reporters:
        yield reporters
