from typing import List

PromptGroup = List[str]


class PromptLibrary:
    answers: PromptGroup
    converse: PromptGroup
    coworker: PromptGroup
    extend: PromptGroup
    function: PromptGroup
    refine: PromptGroup
    skip: PromptGroup

    # things that are not prompt groups
    function_example: dict

    def __init__(
        self,
        answers: PromptGroup | None = None,
        converse: PromptGroup | None = None,
        coworker: PromptGroup | None = None,
        extend: PromptGroup | None = None,
        function: PromptGroup | None = None,
        refine: PromptGroup | None = None,
        skip: PromptGroup | None = None,
        function_example: dict | None = None,
    ) -> None:
        self.answers = answers or []
        self.converse = converse or []
        self.coworker = coworker or []
        self.extend = extend or []
        self.function = function or []
        self.refine = refine or []
        self.skip = skip or []

        self.function_example = function_example or {}
