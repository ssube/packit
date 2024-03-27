from typing import List

PromptTemplateValue = List[str]


class PromptTemplate:
    answers: PromptTemplateValue
    converse: PromptTemplateValue
    coworker: PromptTemplateValue
    extend: PromptTemplateValue
    function: PromptTemplateValue
    refine: PromptTemplateValue
    skip: PromptTemplateValue

    def __init__(
        self,
        answers: PromptTemplateValue | None = None,
        converse: PromptTemplateValue | None = None,
        coworker: PromptTemplateValue | None = None,
        extend: PromptTemplateValue | None = None,
        function: PromptTemplateValue | None = None,
        refine: PromptTemplateValue | None = None,
        skip: PromptTemplateValue | None = None,
    ) -> None:
        self.answers = answers or []
        self.converse = converse or []
        self.coworker = coworker or []
        self.extend = extend or []
        self.function = function or []
        self.refine = refine or []
        self.skip = skip or []
