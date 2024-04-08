from typing import Literal

from mistletoe import Document
from mistletoe.block_token import CodeFence, Paragraph
from mistletoe.span_token import LineBreak, RawText

MarkdownBlock = Literal["code", "text"]


def markdown_result(
    value: str, block_type: MarkdownBlock = "code", code_language="python"
) -> list[str]:
    """
    Parse a markdown document and return the code blocks or text blocks.

    TODO: replace code_language with a filter function
    """

    def get_paragraph_text(block: Paragraph | RawText) -> str:
        if isinstance(block, RawText):
            return block.content
        if isinstance(block, LineBreak):
            return "\n"

        return "".join([get_paragraph_text(child) for child in block.children])

    document = Document(value)

    if block_type == "code":
        return [
            block.content.strip()
            for block in document.children
            if isinstance(block, CodeFence) and block.info_string == code_language
        ]
    elif block_type == "text":
        return [
            get_paragraph_text(block)
            for block in document.children
            if isinstance(block, (Paragraph, RawText))
        ]
    else:
        raise ValueError("Invalid block type")
