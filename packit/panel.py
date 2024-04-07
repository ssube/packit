from logging import getLogger
from typing import Any

from packit.agent import Agent, AgentContext
from packit.conditions import condition_threshold_mean
from packit.loops import loop_retry
from packit.results import bool_result
from packit.tracing import trace
from packit.types import ResultParser

logger = getLogger(__name__)


class Panel:
    agents: list[Agent]
    weights: list[int]

    def __init__(self, agents: dict[Agent, int]):
        self.agents = list(agents.keys())
        self.weights = list(agents.values())

    def sample(
        self,
        prompt: str,
        context: AgentContext,
        result_parser: ResultParser = bool_result,
    ) -> dict[str, str]:
        results = {}

        with trace(self.name, "panel") as (report_args, report_output):
            report_args(prompt, context)

            for agent, weight in zip(self.agents, self.weights):
                for i in range(weight):
                    result = loop_retry(
                        agent,
                        prompt,
                        context=context,
                        result_parser=result_parser,
                    )
                    results[f"{agent.name}-{i}"] = result

            report_output(results)

        return results

    def invoke(
        self,
        prompt: str,
        context: AgentContext,
        result_parser=bool_result,
        decision_condition=condition_threshold_mean,
        min_threshold: float = 0.5,
    ) -> tuple[bool, dict[str, str]]:
        results = self.sample(prompt, context, result_parser=result_parser)
        values = list(results.values())

        return decision_condition(min_threshold, *values), results

    def __call__(self, prompt, **kwargs: Any) -> Any:
        return self.invoke(prompt, kwargs)
