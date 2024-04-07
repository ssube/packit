from contextlib import contextmanager
from logging import getLogger

logger = getLogger(__name__)


@contextmanager
def trace(name: str, kind: str = "packit.task"):
    span_name = f"{kind}.{name}"
    logger.debug("tracing span %s", span_name)

    def report_args(*args, **kwargs):
        logger.debug("reporting args %s %s", args, kwargs)

    def report_output(res):
        logger.debug("reporting output %s", res)

    yield report_args, report_output
