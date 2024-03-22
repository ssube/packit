from packit.prompts.mixtral import prompts as mixtral_prompts
from packit.prompts.smaug import prompts as smaug_prompts

PromptTemplates = dict[str, list[str]]

DEFAULT_PROMPTS = smaug_prompts


def get_prompts(model: str) -> PromptTemplates:
    if "mixtral" in model:
        return mixtral_prompts
    elif "smaug" in model:
        return smaug_prompts
    else:
        return DEFAULT_PROMPTS
