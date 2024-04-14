from contextlib import contextmanager
from json import dumps
from logging import getLogger
from os import environ

from opentelemetry.semconv.ai import SpanAttributes, TraceloopSpanKindValues
from traceloop.sdk import Traceloop
from traceloop.sdk.decorators import _should_send_prompts
from traceloop.sdk.tracing import get_tracer
from traceloop.sdk.tracing.tracing import (
    TracerWrapper,
    get_chained_entity_name,
    set_entity_name,
)
from traceloop.sdk.utils import camel_to_snake

logger = getLogger(__name__)


def snake_case(name: str) -> str:
    return camel_to_snake(name).replace(" ", "_").lower()


def init(exporter=None):
    if TracerWrapper.verify_initialized():
        logger.debug("traceloop SDK already initialized")
        return

    disable_batch = environ.get("TRACELOOP_DISABLE_BATCH", "false").lower() == "true"
    logger.debug(
        "initializing traceloop SDK, %s batching",
        "without" if disable_batch else "with",
    )

    Traceloop.init(disable_batch=disable_batch, exporter=exporter)


@contextmanager
def trace(
    name: str,
    kind: str | TraceloopSpanKindValues = TraceloopSpanKindValues.TASK,
):
    if not TracerWrapper.verify_initialized():
        yield lambda *_, **__: None, lambda _: None
        return

    if isinstance(kind, TraceloopSpanKindValues):
        kind = kind.value

    task_name = snake_case(name)
    span_name = f"{kind}.{task_name}"

    with get_tracer() as tracer:
        with tracer.start_as_current_span(span_name) as span:
            chained_entity_name = get_chained_entity_name(task_name)
            set_entity_name(chained_entity_name)
            logger.debug(
                "tracing span %s for entity %s", span_name, chained_entity_name
            )

            span.set_attribute(SpanAttributes.TRACELOOP_SPAN_KIND, kind)
            span.set_attribute(
                SpanAttributes.TRACELOOP_ENTITY_NAME, chained_entity_name
            )

            def report_args(*args, **kwargs):
                try:
                    if _should_send_prompts():
                        span.set_attribute(
                            SpanAttributes.TRACELOOP_ENTITY_INPUT,
                            dumps({"args": args, "kwargs": kwargs}, default=dumper),
                        )
                except TypeError:
                    # Some args might not be serializable
                    logger.warning("failed to serialize args", exc_info=True)

            def report_output(res):
                try:
                    if _should_send_prompts():
                        span.set_attribute(
                            SpanAttributes.TRACELOOP_ENTITY_OUTPUT,
                            dumps(res, default=dumper),
                        )
                except TypeError:
                    logger.warning("failed to serialize output", exc_info=True)

            yield report_args, report_output


def dumper(value):
    from collections import deque

    from packit.agent import Agent

    if isinstance(value, Agent):
        return f"agent.{snake_case(value.name)}"
    elif isinstance(value, deque):
        return list(value)

    raise TypeError(f"unsupported type: {type(value)}")
