from packit.agent import AgentModelMessage

DEFAULT_STOP = {"done": True, "finish_reason": "stop"}


class MockResponse:
    content: str
    response_metadata: dict[str, bool | str]

    def __init__(self, content: str, response_metadata: dict[str, bool | str]):
        self.content = content
        self.response_metadata = response_metadata


class MockLLM:
    index: int
    messages: list[AgentModelMessage]
    replies: list[str]

    def __init__(self, replies: list[str], start_index=0):
        self.index = 0
        self.messages = []
        self.replies = replies

    def invoke(self, messages: list[AgentModelMessage]) -> str:
        self.messages.extend(messages)
        reply = self.replies[self.index]

        self.index = (self.index + 1) % len(self.replies)
        return MockResponse(reply, DEFAULT_STOP)
