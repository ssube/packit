from logging import getLogger
from typing import Any, Dict, List

from packit.agent import Agent, AgentContext
from packit.conditions import condition_threshold_mean
from packit.loops import loop_retry
from packit.results import bool_result
from packit.tracing import SpanKind, trace
from packit.types import PromptType, ResultParser
from packit.utils import make_list

logger = getLogger(__name__)


PanelResult = Dict[str, PromptType]


class Panel:
    agents: List[Agent]
    name: str
    weights: List[int]

    def __init__(
        self,
        agents: Agent | List[Agent],
        name: str | None = None,
        weights: int | List[int] = 1,
    ):
        agent_list = make_list(agents)
        weight_list = make_list(weights)

        if len(agent_list) != len(weight_list):
            # if only one weight is provided, apply it to all agents
            if len(weight_list) == 1:
                weight_list = [weight_list[0]] * len(agent_list)
            else:
                raise ValueError("The number of agents and weights must match.")

        self.agents = agent_list
        self.name = name or "_".join(agent.name for agent in self.agents)
        self.weights = weight_list

    def sample(
        self,
        prompt: PromptType,
        context: AgentContext,
        result_parser: ResultParser = bool_result,
    ) -> PanelResult:
        results = {}

        with trace(f"panel_{self.name}", SpanKind.GROUP) as (
            report_args,
            report_output,
        ):
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
        prompt: PromptType,
        context: AgentContext,
        result_parser=bool_result,
        decision_condition=condition_threshold_mean,
        min_threshold: float = 0.5,
    ) -> tuple[bool, PanelResult]:
        results = self.sample(prompt, context, result_parser=result_parser)
        values = list(results.values())

        return decision_condition(min_threshold, *values), results

    def __call__(self, prompt, **kwargs: Any) -> Any:
        return self.invoke(prompt, kwargs)
