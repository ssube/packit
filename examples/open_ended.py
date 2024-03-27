"""
Generate and run some code.

Warning: This example can be dangerous if unsupervised. Make sure to validate the generated code before running it.
"""

from packit.agent import Agent, agent_easy_connect
from packit.results import markdown_result
from packit.utils import logger_with_colors

logger = logger_with_colors(__name__)

# Set up a programming expert
llm = agent_easy_connect(model="knoopx/hermes-2-pro-mistral:7b-q8_0", temperature=0.25)
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


# Generate code for some tasks, then use the generated tools
result = programmer(
    "Do something interesting with Python. Have some fun! "
    "Make sure you import any packages that you use. Do not use the art or turtle modules. numpy, pillow, requests, and scipy are available. "
    "Check the syntax before responding. Only return Python code, do not return any other text."
)
logger.info("Raw result: %s", result)

result = programmer(
    "Check the syntax of the following Python program and fix any errors that you find. "
    "Do not run the program, only fix the syntax errors. If the program is correct, respond with the source code. "
    "The program's code is: {code}",
    code=result,
)

# Make sure we have some code blocks
if "```" not in result:
    result = f"```python\n{result}\n```"

# Extract the first code block
code_blocks = markdown_result(result)
if len(code_blocks) == 0:
    logger.error("No code blocks found")
    exit()

block = code_blocks[0]
logger.info("Code block: %s", block)

# Run the generated code
new_tools = create_python_tool(block)
if isinstance(new_tools, str):
    logger.error("Error creating tool: %s", new_tools)
    exit()

logger.info("New tools: %s", new_tools)
for tool in new_tools:
    if tool.__name__ == "main":
        logger.info("Running main function")
        tool()
