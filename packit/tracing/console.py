from contextlib import contextmanager
from logging import getLogger

from .spans import SpanKind

logger = getLogger(__name__)


@contextmanager
def trace(name: str, kind: str | SpanKind = SpanKind.TASK):
    if isinstance(kind, SpanKind):
        kind = kind.value

    span_name = f"{kind}.{name}"
    logger.debug("tracing span %s", span_name)

    def report_args(*args, **kwargs):
        logger.debug("reporting args %s %s", args, kwargs)

    def report_output(res):
        logger.debug("reporting output %s", res)

    yield report_args, report_output
