from random import randint

from langchain_core.utils.function_calling import convert_to_openai_tool

from packit.agent import Agent, agent_easy_connect
from packit.prompts import get_function_example, get_random_prompt
from packit.results import bool_result, function_result
from packit.tools import multiply_tool, sum_tool
from packit.utils import logger_with_colors

# Set up logging
logger = logger_with_colors(__name__)

# Set up some basic tools
tools = [
    convert_to_openai_tool(multiply_tool),
    convert_to_openai_tool(sum_tool),
]
tool_dict = {
    "multiply_tool": multiply_tool,
    "sum_tool": sum_tool,
}

# Connect to two different models
manager_llm = agent_easy_connect(model="mixtral")
function_llm = agent_easy_connect(
    model="knoopx/hermes-2-pro-mistral:7b-q8_0", override_model=True
)

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
)

# Pick two random numbers
a = randint(1, 100)
b = randint(1, 100)

# Ask the manager to prepare a prompt for the tech support agent
question = manager(
    # "You are having trouble with a function call and need help. "
    "You need to multiply two numbers together. The first number is {a} and the second number is {b}. "
    "Ask the tech support agent to find and use the correct function to solve your problem. "
    "Do not introduce yourself or sign the message. Be clear and concise. ",
    a=a,
    b=b,
)
logger.info("Question: %s", question)

# Ask the tech support agent to solve the problem
result = tech_support(
    question + get_random_prompt("function"),
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

# Ask the manager if the result is correct
decision = manager(
    # "You are having trouble with a function call and asked tech support for help. "
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
    if (a * b) == result:
        logger.info("The manager accepted the correct result.")
    else:
        logger.error("The manager accepted an incorrect result.")
else:
    if (a * b) == result:
        logger.error("The manager rejected the correct result.")
    else:
        logger.info("The manager rejected an incorrect result.")
