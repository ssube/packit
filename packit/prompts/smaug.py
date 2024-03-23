function_call = {
    "function": "multiply",
    "parameters": {"a": 3, "b": 8},
}

prompts = {
    "function": [
        "Given the following JSON object, please respond with a valid function call in JSON syntax. "
        "For example: {example}. "
        "Do not implement the function or include code for the body of the function. Only call the function once. "
        "Do not introduce yourself or sign the message. Be clear and concise. "
        "Fill in all of the parameters with valid values, according to their type and description. "
        "Make sure you fill in all of the required parameters. "
        "The available functions are: {tools}"
    ],
    "refine": [
        "Take the following text and improve on it. Fix any typos, grammatical errors, or syntax errors.",
    ],
    "skip": [
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
}
