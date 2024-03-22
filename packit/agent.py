from logging import getLogger
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from packit.formats import format_str_or_json
from packit.prompts import DEFAULT_PROMPTS, PromptTemplates

logger = getLogger(__name__)


AgentContext = dict[str, str]
AgentModelMessage = HumanMessage | SystemMessage


class AgentModel:
    def invoke(self, prompt, **kwargs):
        pass


class Agent:
    backstory: str
    context: AgentContext
    llm: type[AgentModel]
    name: str

    def __init__(self, name, backstory, context, llm):
        self.backstory = backstory
        self.context = context
        self.llm = llm
        self.name = name

    def invoke_retry(
        self,
        messages: list[AgentModelMessage],
        max_retry: int = 3,
        prompt_templates: PromptTemplates = DEFAULT_PROMPTS,
    ):
        retry = 0
        while retry < max_retry:
            retry += 1
            result = self.llm.invoke(messages)
            if not self.response_complete(result):
                logger.warning("LLM did not finish: %s", result)
                # TODO: get the rest of the response

            do_skip = False
            for skip_token in prompt_templates["skip"]:
                if skip_token in result.content:
                    logger.warning(
                        "found skip token %s, skipping response: %s", skip_token, result
                    )
                    do_skip = True

            if do_skip:
                continue

            return result

        logger.warning("failed to get a valid response from agent")
        return result

    def invoke(self, prompt: str, context: AgentContext) -> str:
        args = {}
        args.update(self.context)
        args.update(context)
        args = {k: format_str_or_json(v) for k, v in args.items()}

        formatted_prompt = prompt.format(**args)
        formatted_backstory = self.backstory.format(**args)

        logger.info("System: %s", formatted_backstory)
        logger.info("Prompt: %s", formatted_prompt)
        messages = [
            SystemMessage(content=formatted_backstory),
            HumanMessage(content=formatted_prompt),
        ]

        result = self.invoke_retry(messages)

        if not self.response_complete(result):
            logger.warning("LLM did not finish: %s", result)

        return result.content

    def response_complete(self, result: Any) -> bool:
        if "done" in result.response_metadata:
            return result.response_metadata["done"]

        if "finish_reason" in result.response_metadata:
            return result.response_metadata["finish_reason"] == "stop"

        return False

    def __call__(self, prompt: str, **kwargs: Any) -> str:
        return self.invoke(prompt, kwargs)
