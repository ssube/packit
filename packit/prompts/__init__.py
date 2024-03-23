from random import choice
from typing import Literal

from .mixtral import (
    prompts as mixtral_prompts,
    function_call as mixtral_function_call,
)
from .smaug import prompts as smaug_prompts

PromptTemplateKey = Literal["converse", "extend", "function", "refine", "skip"]
PromptTemplates = dict[PromptTemplateKey, list[str]]

DEFAULT_PROMPTS = mixtral_prompts


def get_function_example() -> dict[str, dict[str, int]]:
    return mixtral_function_call


def get_prompts(model: str) -> PromptTemplates:
    if "mixtral" in model:
        return mixtral_prompts
    elif "smaug" in model:
        return smaug_prompts
    else:
        return DEFAULT_PROMPTS


def get_random_prompt(key: PromptTemplateKey) -> str:
    return choice(DEFAULT_PROMPTS[key])


def set_default_prompts(prompts: PromptTemplates):
    global DEFAULT_PROMPTS
    DEFAULT_PROMPTS = prompts
