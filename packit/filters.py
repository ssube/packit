from packit.memory import make_limited_memory


def repeat_prompt_filter(
    error_prompt: str,
    search_window: int = 10,
):
    """
    Filter out repeated prompts.
    """

    memory = make_limited_memory(search_window)

    def filter_fn(value: str) -> str | None:
        if value in memory:
            return error_prompt

        memory.append(value)
        return None

    def clear_memory():
        memory.clear()

    return filter_fn, clear_memory


def repeat_tool_filter(
    error_prompt: str,
    search_window: int = 10,
):
    """
    Filter out repeated tool calls.
    """

    memory = make_limited_memory(search_window)

    def filter_fn(value: dict) -> str | None:
        if value in memory:
            return error_prompt

        memory.append(value)
        return None

    def clear_memory():
        memory.clear()

    return filter_fn, clear_memory
