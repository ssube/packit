from unittest import TestCase

from opentelemetry.sdk.trace.export import ConsoleSpanExporter

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
