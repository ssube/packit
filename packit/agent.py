from logging import getLogger
from os import environ
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

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
    memory: list[AgentModelMessage] | None
    memory_limit: int
    name: str

    def __init__(self, name, backstory, context, llm, memory=True, memory_limit=10):
        self.backstory = backstory
        self.context = context
        self.llm = llm
        self.name = name

        if memory:
            self.memory = []
            self.memory_limit = memory_limit
        else:
            self.memory = None
            self.memory_limit = 0

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

        logger.debug("System: %s", formatted_backstory)
        logger.debug("Prompt: %s", formatted_prompt)

        system = SystemMessage(content=formatted_backstory)
        human = HumanMessage(content=formatted_prompt)

        if self.memory is not None:
            logger.debug("Memory: %s", self.memory)
            messages = [
                system,
                *self.memory,
                human,
            ]
        else:
            messages = [
                system,
                human,
            ]

        result = self.invoke_retry(messages)

        if not self.response_complete(result):
            logger.warning("LLM did not finish: %s", result)

        reply = result.content
        logger.debug("Response: %s", reply)

        if self.memory is not None:
            self.memory.append(human)
            self.memory.append(AIMessage(content=reply))
            if len(self.memory) > self.memory_limit:
                self.memory = self.memory[-self.memory_limit :]

        return reply

    def response_complete(self, result: Any) -> bool:
        if "done" in result.response_metadata:
            return result.response_metadata["done"]

        if "finish_reason" in result.response_metadata:
            return result.response_metadata["finish_reason"] == "stop"

        return False

    def __call__(self, prompt: str, **kwargs: Any) -> str:
        return self.invoke(prompt, kwargs)


def agent_easy_connect(
    driver: str = "openai", model: str = "gpt-4", temperature: float = 0.0
) -> AgentModel:
    """
    Quick connect to one of a few pre-defined LLMs using common environment variables.

    This has very limited features and is mostly for testing and the examples.
    """
    driver = environ.get("PACKIT_DRIVER", driver)
    model = environ.get("PACKIT_MODEL", model)

    if driver == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model, temperature=temperature)
    elif driver == "ollama":
        from langchain_community.chat_models import ChatOllama

        ollama_api = environ.get("OLLAMA_API", "http://localhost:11434")
        num_ctx = environ.get("OLLAMA_NUM_CTX", 2048)
        num_gpu = environ.get("OLLAMA_NUM_GPU", 20)

        return ChatOllama(
            model=model,
            temperature=temperature,
            base_url=ollama_api,
            num_ctx=num_ctx,
            num_gpu=num_gpu,
        )
    else:
        raise ValueError(f"Unknown driver: {driver}")
