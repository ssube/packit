from packit.agent import Agent
from packit.errors import ToolError
from packit.loops import loop_retry
from packit.types import ResultParser


def make_team_tools(team: list[Agent], result_parser: ResultParser | None = None):
    names = [agent.name for agent in team]

    def delegate_tool(
        coworker: str, task: str, context: dict[str, str] | None = None
    ) -> str:
        """
        Delegate a task to a coworker.

        Args:
            coworker: The name of the coworker.
            task: The task for the coworker to complete.
        """

        context = context or {}

        for agent in team:
            if agent.name == coworker:
                return loop_retry(
                    agent,
                    task,
                    context=context,
                    result_parser=result_parser,
                    toolbox=agent.toolbox,
                )

        raise ToolError(
            f"I'm sorry, that coworker does not exist. Available coworkers: {', '.join(names)}.",
            agent,
            task,
            delegate_tool.__name__,
        )

    def question_tool(
        coworker: str, question: str, context: dict[str, str] | None = None
    ) -> str:
        """
        Ask a question of a coworker.

        Args:
            coworker: The name of the coworker.
            question: The question to ask the coworker.
        """

        context = context or {}

        for agent in team:
            if agent.name == coworker:
                return loop_retry(
                    agent,
                    question,
                    context=context,
                    result_parser=result_parser,
                    toolbox=agent.toolbox,
                )

        raise ToolError(
            f"I'm sorry, that coworker does not exist. Available coworkers: {', '.join(names)}.",
            agent,
            question,
            question_tool.__name__,
        )

    return delegate_tool, question_tool
