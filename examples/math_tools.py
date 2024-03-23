from json import dumps
from random import randint

from langchain_core.utils.function_calling import convert_to_openai_tool

from packit.agent import Agent, agent_easy_connect
from packit.results import function_result
from packit.tools import lowercase_tool, multiply_tool, sum_tool, uppercase_tool

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
llm = agent_easy_connect()
agent = Agent(
    "programmer",
    "You are an expert computer programmer with a lot of experience.",
    {},
    llm,
)

# Ask the agent to multiply two random numbers
a = randint(1, 100)
b = randint(1, 100)
print("Multiplying:", a, b)

example_call = {
    "function": "multiply",
    "parameters": {"a": 3, "b": 8},
}

# Do some multiplication
prompt = (
    "Multiply {a} by {b}. "
    "Given the following JSON object, please respond with a valid function call in JSON syntax. "
    "For example: {example}. "
    "Do not implement the function or include code for the body of the function. Only call the function once. "
    "Fill in all of the parameters with valid values, according to their type and description. "
    "Make sure you fill in all of the required parameters. "
    "The available functions are: {tools}"
)
result = agent(prompt, a=a, b=b, example=dumps(example_call), tools=dumps(tools))
print("Raw result:", result)

result = function_result(
    result,
    tool_dict,
)
print("Multiply result:", result)
print("Correct result:", a * b)

# Do some sums
for i in range(2, 6):
    numbers = [randint(1, 100) for _ in range(i)]
    print("Summing:", numbers)

    prompt = (
        "Sum up the following numbers: {numbers}. "
        "Given the following JSON object, please respond with a valid function call in JSON syntax. "
        "For example: {example}. "
        "Do not implement the function or include code for the body of the function. Only call the function once. "
        "Fill in all of the parameters with valid values, according to their type and description. "
        "Make sure you fill in all of the required parameters. "
        "The available functions are: {tools}"
    )
    result = agent(
        prompt, numbers=numbers, example=dumps(example_call), tools=dumps(tools)
    )
    print("Raw result:", result)

    result = function_result(
        result,
        tool_dict,
    )
    print("Sum result:", result)
    print("Correct result:", sum(numbers))
