from langchain_core.utils.function_calling import convert_to_openai_tool

from packit.agent import Agent, agent_easy_connect
from packit.prompts import get_function_example, get_random_prompt
from packit.results import function_result
from packit.tools import lowercase_tool, titlecase_tool, uppercase_tool
from packit.utils import logger_with_colors

# Set up logging
logger = logger_with_colors(__name__)

# Set up some basic tools
tools = [
    convert_to_openai_tool(lowercase_tool),
    convert_to_openai_tool(titlecase_tool),
    convert_to_openai_tool(uppercase_tool),
]
tool_dict = {
    "lowercase_tool": lowercase_tool,
    "titlecase_tool": titlecase_tool,
    "uppercase_tool": uppercase_tool,
}

# Create an agent that uses the tool
llm = agent_easy_connect(model="knoopx/hermes-2-pro-mistral:7b-q8_0")
agent = Agent(
    "programmer",
    "You are an expert computer programmer with a lot of experience.",
    {},
    llm,
)

example_call = {
    "function": "multiply",
    "parameters": {"a": 3, "b": 8},
}

# Convert some strings
inputs = [
    "all lower case words",
    "ALL UPPER CASE WORDS",
    "Mixed Case Words",
]

for input in inputs:
    result = agent(
        "Convert the following string into title case: {input}. "
        + get_random_prompt("function"),
        input=input,
        example=get_function_example(),
        tools=tools,
    )
    logger.info("Raw result: %s", result)

    result = function_result(
        result,
        tool_dict,
    )
    logger.info("Title case result: %s", result)
