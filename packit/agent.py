from logging import getLogger
from os import environ
from typing import Any, Callable, Protocol

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from packit.formats import format_str_or_json
from packit.memory import make_limited_memory, memory_order_width
from packit.prompts import DEFAULT_PROMPTS, PromptTemplate

logger = getLogger(__name__)


AgentContext = dict[str, str]
AgentModelMessage = HumanMessage | SystemMessage


class AgentModel(Protocol):
    def invoke(self, prompts: list[AgentModelMessage], **kwargs):
        pass


class Agent:
    backstory: str
    context: AgentContext
    llm: AgentModel
    max_retry: int
    memory: list[AgentModelMessage] | None
    memory_maker: Callable | None
    name: str

    def __init__(
        self,
        name,
        backstory,
        context,
        llm,
        max_retry=3,
        memory: Callable | None = make_limited_memory,
        memory_maker: Callable | None = memory_order_width,
    ):
        self.backstory = backstory
        self.context = context
        self.llm = llm
        self.max_retry = max_retry
        self.memory_maker = memory_maker
        self.name = name

        if memory:
            self.memory = memory()
        else:
            self.memory = None

    def invoke_retry(
        self,
        messages: list[AgentModelMessage],
        prompt_templates: PromptTemplate = DEFAULT_PROMPTS,
    ):
        retry = 0
        while retry < self.max_retry:
            retry += 1
            result = self.llm.invoke(messages)
            if not self.response_complete(result):
                logger.warning("LLM did not finish: %s", result)
                # TODO: get the rest of the response

            do_skip = False
            for skip_token in prompt_templates.skip:
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

    def invoke(
        self,
        prompt: str,
        context: AgentContext,
        prompt_templates: PromptTemplate = DEFAULT_PROMPTS,
    ) -> str:
        args = {}
        args.update(self.context)
        args.update(context)
        args = {k: format_str_or_json(v) for k, v in args.items()}

        try:
            formatted_prompt = prompt.format(**args)
            formatted_backstory = self.backstory.format(**args)
        except Exception as e:
            logger.exception("Error formatting prompt: %s", prompt)
            return f"{type(e).__name__} while formatting prompt: {str(e)}"

        logger.debug("Agent: %s", self.name)
        logger.debug("System: %s", formatted_backstory)
        logger.debug("Prompt: %s", formatted_prompt)

        system = SystemMessage(content=formatted_backstory)
        human = HumanMessage(content=formatted_prompt)

        if self.memory is not None:
            # logger.debug("Memory: %s", self.memory)
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

        result = self.invoke_retry(messages, prompt_templates=prompt_templates)

        if not self.response_complete(result):
            logger.warning("LLM did not finish: %s", result)

        reply = result.content
        reply = reply.replace("<|im_end|>", "").strip()
        logger.debug("Response: %s", reply)

        if self.memory and self.memory_maker:
            self.memory_maker(self.memory, human)
            self.memory_maker(self.memory, AIMessage(content=reply))

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
    driver: str = "openai",
    model: str = "gpt-4",
    override_model: bool = False,
    temperature: float = 0.0,
) -> AgentModel:
    """
    Quick connect to one of a few pre-defined LLMs using common environment variables.

    This has very limited features and is mostly for testing and the examples.
    """
    driver = environ.get("PACKIT_DRIVER", driver)

    if not override_model:
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
