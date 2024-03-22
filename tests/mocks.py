DEFAULT_STOP = {"done": True, "finish_reason": "stop"}


class MockResponse:
    content: str
    response_metadata: dict[str, bool | str]

    def __init__(self, content: str, response_metadata: dict[str, bool | str]):
        self.content = content
        self.response_metadata = response_metadata


class MockLLM:
    replies: list[str]

    def __init__(self, replies: list[str]):
        self.replies = replies

    def invoke(self, messages: list[str]) -> str:
        reply = self.replies.pop(0)
        return MockResponse(reply, DEFAULT_STOP)
