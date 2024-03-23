from random import randint

from langchain_core.utils.function_calling import convert_to_openai_tool

from packit.agent import Agent, agent_easy_connect
from packit.results import function_result, bool_result
from packit.tools import multiply_tool, sum_tool

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
)

# Pick two random numbers
a = randint(1, 100)
b = randint(1, 100)

# Ask the manager to prepare a prompt for the tech support agent
question = manager(
    "You are having trouble with a function call and need help. "
    "You need to multiply two numbers together. The first number is {a} and the second number is {b}. "
    "Ask the tech support agent to find and use the correct function to solve your problem. "
    "Do not introduce yourself or sign the message. Be clear and concise. ",
    a=a,
    b=b,
)
print("Question:", question)

# Ask the tech support agent to solve the problem
example_call = {
    "function": "multiply",
    "parameters": {"a": 3, "b": 8},
}

function_prompt = (
    "Given the following JSON object, please respond with a valid function call in JSON syntax. "
    "For example: {example}. "
    "Do not implement the function or include code for the body of the function. Only call the function once. "
    "Do not introduce yourself or sign the message. Be clear and concise. "
    "Fill in all of the parameters with valid values, according to their type and description. "
    "Make sure you fill in all of the required parameters. "
    "The available functions are: {tools}"
)
result = tech_support(
    question + function_prompt,
    example=example_call,
    tools=tools,
)
print("Raw result:", result)

result = function_result(
    result,
    tool_dict,
)
print("Multiply result:", result)
print("Correct result:", a * b)

# Ask the manager if the result is correct
decision = manager(
    "You are having trouble with a function call and asked tech support for help. "
    "You need to multiply two numbers together. The first number is {a} and the second number is {b}. "
    "The tech support agent has provided the result: {result}. "
    "Is this the correct result? Reply with a one word answer: 'yes' or 'no'.",
    a=a,
    b=b,
    result=result,
)
print("Decision:", decision)

# Compare the outputs
if bool_result(decision):
    if (a * b) == result:
        print("The manager accepted the correct result.")
    else:
        print("The manager accepted an incorrect result.")
else:
    if (a * b) == result:
        print("The manager rejected the correct result.")
    else:
        print("The manager rejected an incorrect result.")
