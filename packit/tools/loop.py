from logging import getLogger

logger = getLogger(__name__)


def make_complete_tool():
    """
    Make a tool to complete tasks and exit the loop.
    """
    complete = False
    result = None

    def complete_tool(answer: str) -> str:
        """
        Complete a task.

        Args:
            answer: The answer to the task.
        """
        nonlocal complete
        nonlocal result

        complete = True
        result = answer

        logger.info("Answer: %s", answer)
        return "Task complete."

    def complete_condition(*args, **kwargs) -> bool:
        """
        Stop when the task is complete.
        """
        return complete

    def get_result() -> str:
        return result

    def reset_complete() -> None:
        nonlocal complete
        complete = False

    return complete_tool, complete_condition, get_result, reset_complete
