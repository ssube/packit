from random import randint

from packit.agent import Agent, agent_easy_connect
from packit.loops import loop_tool
from packit.results import bool_result
from packit.toolbox import Toolbox
from packit.tools import multiply_tool, sum_tool
from packit.utils import logger_with_colors

# Set up logging
logger = logger_with_colors(__name__)

# Set up some basic tools
toolbox = Toolbox(
    [
        multiply_tool,
        sum_tool,
    ]
)

# Connect to two different models
manager_llm = agent_easy_connect(model="mixtral")
function_llm = agent_easy_connect(model="knoopx/hermes-2-pro-mistral:7b-q8_0")

# Set up agents for each role
manager = Agent(
    "manager",
    "You are an experienced business manager with a collaborative team.",
    {},
    manager_llm,
)

tech_support = Agent(
    "tech_support",
    "You are an expert in technical support and helping coworkers call the right functions to solve their problems.",
    {},
    function_llm,
    toolbox=toolbox,
)

# Pick two random numbers
a = randint(1, 100)
b = randint(1, 100)

# Ask the manager to prepare a prompt for the tech support agent
question = manager(
    "You need to multiply two numbers together. The first number is {a} and the second number is {b}. "
    "Ask the tech support agent to find and use the correct function to solve your problem. "
    "Do not introduce yourself or sign the message. Be clear and concise. ",
    a=a,
    b=b,
)
logger.info("Question: %s", question)

# Ask the tech support agent to solve the problem
result = loop_tool(tech_support, question, toolbox=toolbox)
logger.info("Multiply result: %s", result)
logger.info("Correct result: %s", a * b)

# Ask the manager if the result is correct
decision = manager(
    "You need to multiply two numbers together. The first number is {a} and the second number is {b}. "
    "The tech support agent has provided this result: {result}. "
    "Is this the correct result? Reply with a one word answer: 'yes' or 'no'.",
    a=a,
    b=b,
    result=result,
)
logger.info("Decision: %s", decision)

# Compare the outputs
if bool_result(decision):
    if str(a * b) == result:
        logger.info("The manager accepted the correct result.")
    else:
        logger.error("The manager accepted an incorrect result.")
else:
    if str(a * b) == result:
        logger.error("The manager rejected the correct result.")
    else:
        logger.info("The manager rejected an incorrect result.")
