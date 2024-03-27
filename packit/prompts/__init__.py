from random import choice

from .base import PromptTemplate
from .mixtral import (
    prompts as mixtral_prompts,
    function_call as mixtral_function_call,
)
from .smaug import prompts as smaug_prompts

DEFAULT_PROMPTS = mixtral_prompts


def get_function_example() -> dict[str, dict[str, int]]:
    return mixtral_function_call


def get_prompts(model: str) -> PromptTemplate:
    if "mixtral" in model:
        return mixtral_prompts
    elif "smaug" in model:
        return smaug_prompts
    else:
        return DEFAULT_PROMPTS


def get_random_prompt(key: str) -> str:
    if hasattr(DEFAULT_PROMPTS, key):
        prompts = getattr(DEFAULT_PROMPTS, key)
        return choice(prompts)

    raise KeyError(f"Prompt key '{key}' not found in default prompts.")


def set_default_prompts(prompts: PromptTemplate):
    global DEFAULT_PROMPTS
    DEFAULT_PROMPTS = prompts
