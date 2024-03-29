"""
Generate and run some code.

Warning: This example can be dangerous if unsupervised. Make sure to validate the generated code before running it.
"""

from packit.agent import Agent, agent_easy_connect
from packit.loops import loop_tool
from packit.results import markdown_result
from packit.toolbox import Toolbox
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
task_template = (
    "Write a Python function to {task}. Only generate the function definition, do not call it. "
    "Only generate a single function, do not include any other code."
)
task_prompts = [
    "calculate the factorial of a number",
    "download the Wikipedia homepage and save it to a file",
    "plot a graph of a mathematical function",
    "load a CSV file and display the first 5 rows",
    "call a JSON API and display the title and body of the last 3 posts",
]
usage_prompts = [
    "Call the function you just wrote with a random number.",
    "Call the function you just wrote with a filename of /tmp/wiki.html.",
    "Call the function you just wrote with a linear function.",
    "Call the function you just wrote with a filename of /tmp/data.csv.",
    "Call the function you just wrote with the posts from https://jsonplaceholder.typicode.com/posts.",
]

for task, usage in zip(task_prompts, usage_prompts):
    result = programmer(task_template, task=task)
    logger.info("Raw result: %s", result)

    # Make sure we have some code blocks
    if "```" not in result:
        result = f"```python\n{result}\n```"

    # Extract the first code block
    code_blocks = markdown_result(result)
    if len(code_blocks) == 0:
        logger.error("No code blocks found")
        continue

    block = code_blocks[0]
    logger.info("Code block: %s", block)

    # Create a new tool from the generated code
    try:
        new_tools = create_python_tool(block)
        if isinstance(new_tools, str):
            logger.error("Error creating tool: %s", new_tools)
            continue

        # Prepare a toolbox with the generated tools
        logger.info("New tools: %s", [tool.__name__ for tool in new_tools])
        toolbox = Toolbox([*new_tools, create_python_tool])

        # Get the factorial of a random number
        result = loop_tool(programmer, usage, toolbox=toolbox)
        logger.info("Result: %s", result)
    except Exception:
        logger.exception("Error running generated code")
