from random import randint

from packit.agent import Agent, agent_easy_connect
from packit.loops import loop_tool
from packit.toolbox import Toolbox
from packit.tools import lowercase_tool, multiply_tool, sum_tool, uppercase_tool
from packit.utils import logger_with_colors

# Set up logging
logger = logger_with_colors(__name__)

# Set up some basic tools, with a few extras that should not be used
toolbox = Toolbox(
    [
        lowercase_tool,
        multiply_tool,
        sum_tool,
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

# Ask the agent to multiply two random numbers
a = randint(1, 100)
b = randint(1, 100)
logger.info("Multiplying: %s * %s", a, b)

# Do some multiplication
result = loop_tool(
    agent,
    "Multiply {a} by {b}.",
    context={"a": a, "b": b},
    toolbox=toolbox,
)
logger.info("Multiply result: %s", result)
logger.info("Correct result: %s", a * b)

# Do some sums
for i in range(2, 6):
    numbers = [randint(1, 100) for _ in range(i)]
    logger.info("Summing: %s", numbers)

    result = loop_tool(
        agent,
        "Sum up the following numbers: {numbers}.",
        context={"numbers": numbers},
        toolbox=toolbox,
    )
    logger.info("Sum result: %s", result)
    logger.info("Correct result: %s", sum(numbers))
