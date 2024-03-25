from packit.agent import Agent


def make_team_tools(team: list[Agent]):
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
                return agent(task, **context)

        return "I'm sorry, that coworker does not exist."

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
                return agent(question, **context)

        return "I'm sorry, that coworker does not exist."

    return delegate_tool, question_tool
