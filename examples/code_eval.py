"""
Generate and run some code.

Warning: This example can be dangerous if unsupervised. Make sure to validate the generated code before running it.
"""

from random import randint

from packit.agent import Agent, agent_easy_connect
from packit.prompts import get_function_example, get_random_prompt
from packit.results import function_result, markdown_result
from packit.tools import Toolbox
from packit.utils import logger_with_colors

logger = logger_with_colors(__name__)

# Set up a programming expert
llm = agent_easy_connect(model="mixtral", temperature=0.25)
programmer = Agent(
    "programmer",
    "You are an expert computer programmer with a focus on Python and deep understanding of algorithms.",
    {},
    llm,
)


# Prepare a function to safely run Python code
def create_python_tool(value: str) -> str:
    confirm = input("Are you sure you want to run this code? (y/n): ")
    if confirm.lower() != "y":
        return "The generated code was dangerous and could not be executed."

    exec_scope = {}
    try:
        exec(value, exec_scope)
    except Exception as e:
        return f"Error: {e}"

    return [f for f in exec_scope.values() if callable(f)]


# Generate some code
result = programmer(
    "Write a Python function that calculates the factorial of a number."
)
logger.info("Raw result: %s", result)

code_blocks = markdown_result(result)
for block in code_blocks:
    logger.info("Code block: %s", block)
    new_tools = create_python_tool(block)
    logger.info("New tools: %s", [tool.__name__ for tool in new_tools])

    # Prepare a toolbox with the generated tools
    toolbox = Toolbox([*new_tools, create_python_tool])

    # Get the factorial of a random number
    number = randint(1, 100)
    result = programmer(
        "Using the function you just wrote, calculate the factorial of {n}. "
        + get_random_prompt("function"),
        example=get_function_example(),
        n=number,
        tools=toolbox.definitions,
    )

    logger.info("Raw result: %s", result)
    factorial = function_result(result, toolbox.callbacks)
    logger.info("Factorial of %s: %s", number, factorial)
