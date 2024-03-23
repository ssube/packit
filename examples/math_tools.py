from random import randint

from langchain_core.utils.function_calling import convert_to_openai_tool

from packit.agent import Agent, agent_easy_connect
from packit.prompts import get_function_example, get_random_prompt
from packit.results import function_result
from packit.tools import lowercase_tool, multiply_tool, sum_tool, uppercase_tool
from packit.utils import logger_with_colors

# Set up logging
logger = logger_with_colors(__name__)

# Set up some basic tools
tools = [
    convert_to_openai_tool(lowercase_tool),
    convert_to_openai_tool(multiply_tool),
    convert_to_openai_tool(sum_tool),
    convert_to_openai_tool(uppercase_tool),
]
tool_dict = {
    "lowercase_tool": lowercase_tool,
    "multiply_tool": multiply_tool,
    "sum_tool": sum_tool,
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

# Ask the agent to multiply two random numbers
a = randint(1, 100)
b = randint(1, 100)
logger.info("Multiplying: %s * %s", a, b)

# Do some multiplication
result = agent(
    "Multiply {a} by {b}. " + get_random_prompt("function"),
    a=a,
    b=b,
    example=get_function_example(),
    tools=tools,
)
logger.info("Raw result: %s", result)

result = function_result(
    result,
    tool_dict,
)
logger.info("Multiply result: %s", result)
logger.info("Correct result: %s", a * b)

# Do some sums
for i in range(2, 6):
    numbers = [randint(1, 100) for _ in range(i)]
    logger.info("Summing:", numbers)

    result = agent(
        "Sum up the following numbers: {numbers}. " + get_random_prompt("function"),
        numbers=numbers,
        example=get_function_example(),
        tools=tools,
    )
    logger.info("Raw result: %s", result)

    result = function_result(
        result,
        tool_dict,
    )
    logger.info("Sum result: %s", result)
    logger.info("Correct result: %s", sum(numbers))
