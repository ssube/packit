from .base import PromptLibrary

function_call = {
    "function": "multiply",
    "parameters": {"a": 3, "b": 8},
}

prompts = PromptLibrary(
    answers=[
        "Your coworkers have provided the following answers: {history}.",
    ],
    converse=[
        "What do you think about this?",
    ],
    coworker=[
        "Your team includes coworkers named: {coworkers}.",
    ],
    extend=[
        "How would you continue this?",
        "What would you add to this?",
        "Expand on this idea and provide more details.",
    ],
    function=[
        "Given the following JSON object, please respond with a valid function call in JSON syntax. "
        "For example: {example}. "
        "Do not implement the function or include code for the body of the function. Only call the function once. "
        "Do not introduce yourself or sign the message. Be clear and concise. "
        "Fill in all of the parameters with valid values, according to their type and description. "
        "Make sure you fill in all of the required parameters. "
        "The available functions are: {tools}"
    ],
    function_example=function_call,
    refine=[
        "Take the following text and improve on it. Fix any typos, grammatical errors, or syntax errors.",
    ],
    skip=[
        "<|endoftext|>",
        "<|assistant|>",
        "</|assistant|>",
        "<|human|>",
        "</|human|>",
        "<|user|>",
        "</|user|>",
        "<|system|>",
        "</|system|>",
        "<s>",
        "</s>",
    ],
)
