from packit.agent import Agent


class PromptError(Exception):
    agent: Agent
    prompt: str

    def __init__(self, message: str, agent: Agent, prompt: str):
        super().__init__(message)
        self.agent = agent
        self.prompt = prompt


class ToolError(PromptError):
    tool: str

    def __init__(self, message: str, agent: Agent, prompt: str, tool: str):
        super().__init__(message, agent, prompt)
        self.tool = tool
