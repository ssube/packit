from langchain_core.utils.function_calling import convert_to_openai_tool


def prepare_tools(tools) -> tuple[list[dict], dict[str, callable]]:
    """
    Convert a list of functions into Langchain-compatible tools and return them along with a dictionary of callbacks.
    """

    # Initialize the tool dictionary
    tool_definitions = []
    tool_callbacks = {}

    # Iterate over the tools
    for tool in tools:
        name = tool.__name__
        tool_callbacks[name] = tool

        tool_definitions.append(convert_to_openai_tool(tool))

    # Return the metadata and tool callbacks
    return tool_definitions, tool_callbacks
