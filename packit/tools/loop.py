from typing import Callable


def make_complete_tool() -> tuple[Callable, Callable]:
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

        return "Task complete."

    def complete_condition(*args) -> bool:
        """
        Stop when the task is complete.
        """
        return complete

    return complete_tool, complete_condition
