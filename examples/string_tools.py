from packit.agent import Agent, agent_easy_connect
from packit.loops import loop_tool
from packit.toolbox import Toolbox
from packit.tools import lowercase_tool, titlecase_tool, uppercase_tool
from packit.utils import logger_with_colors

# Set up logging
logger = logger_with_colors(__name__)

# Set up some basic tools
toolbox = Toolbox(
    [
        lowercase_tool,
        titlecase_tool,
        uppercase_tool,
    ]
)

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
    result = loop_tool(
        agent,
        "Convert the following string into title case: {input}. ",
        context={"input": input},
        toolbox=toolbox,
    )
    logger.info("Title case result: %s", result)
