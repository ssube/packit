from unittest import TestCase

from opentelemetry.sdk.trace.export import ConsoleSpanExporter

from packit.tracing import set_tracer
from packit.tracing.traceloop import init, trace


class TestTraceloopInit(TestCase):
    def test_init(self):
        self.assertIsNone(init())


class TestTraceloopTrace(TestCase):
    def test_trace(self):
        init(exporter=ConsoleSpanExporter())
        with trace("name", "kind") as (report_args, report_output):
            self.assertIsNone(report_args())
            self.assertIsNone(report_output("test"))


class TestSetTrace(TestCase):
    def test_set_console_tracer(self):
        self.assertIsNone(set_tracer("console"))
        # TODO: make sure the tracer is set to console

    def test_set_traceloop_tracer(self):
        self.assertIsNone(set_tracer("traceloop"))
        # TODO: make sure the tracer is set to traceloop

    def test_set_callable_tracer(self):
        self.assertIsNone(set_tracer(lambda: None))
        # TODO: make sure the tracer is set to the callable

    def test_set_invalid_tracer(self):
        with self.assertRaises(ValueError):
            set_tracer("invalid")
