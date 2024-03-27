from logging import getLogger

logger = getLogger(__name__)


def make_complete_tool():
    """
    Make a tool to complete tasks and exit the loop.

    TODO: provide a way to access the task answer.
    """
    complete = False

    def complete_tool(answer: str) -> str:
        """
        Complete a task.

        Args:
            answer: The answer to the task.
        """
        nonlocal complete
        complete = True

        logger.info("Answer: %s", answer)
        return "Task complete."

    def complete_condition(*args) -> bool:
        """
        Stop when the task is complete.
        """
        return complete

    def reset_complete() -> None:
        nonlocal complete
        complete = False

    return complete_tool, complete_condition, reset_complete
