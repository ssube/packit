from json import dumps

from langchain_core.utils.function_calling import convert_to_openai_tool

from packit.agent import Agent, agent_easy_connect
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
llm = agent_easy_connect()
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
    prompt = (
        "Convert the following string into title case: {input}. "
        "Given the following JSON object, please respond with a valid function call in JSON syntax. "
        "For example: {example}. "
        "Do not implement the function or include code for the body of the function. Only call the function once. "
        "Fill in all of the parameters with valid values, according to their type and description. "
        "Make sure you fill in all of the required parameters. "
        "If none of the available functions can be used to solve the problem, please respond with 'none'. "
        "The available functions are: {tools}"
    )
    result = agent(prompt, input=input, example=dumps(example_call), tools=dumps(tools))
    logger.info("Raw result:", result)

    result = function_result(
        result,
        tool_dict,
    )
    logger.info("Title case result:", result)
