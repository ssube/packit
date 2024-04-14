from typing import List, Literal, Union

from mistletoe import Document
from mistletoe.block_token import CodeFence, Heading, Paragraph
from mistletoe.span_token import LineBreak, RawText

from packit.utils import flatten

MarkdownBlock = Literal["code", "text"]

BlockResult = str | None
SelectorResult = (
    List[Union[BlockResult, "SelectorResult"]] | BlockResult
)  # inner type has to use Union because of the forward reference


def select_text_blocks(block: Paragraph | RawText, headers=False) -> SelectorResult:
    if isinstance(block, LineBreak):
        return "\n"

    if isinstance(block, RawText):
        return block.content

    if isinstance(block, Heading) and not headers:
        return None

    children = [select_text_blocks(child) for child in block.children]
    return [child for child in children if child is not None]


def select_code_blocks(block: CodeFence, language: str = "python") -> SelectorResult:
    if isinstance(block, CodeFence) and block.info_string == language:
        return block.content.strip()

    if not hasattr(block, "children"):
        return None

    children = [select_code_blocks(child) for child in block.children]
    return [child for child in children if child is not None]


def markdown_result(
    value: str,
    selector=select_code_blocks,
) -> list[str]:
    """
    Parse a markdown document and return the code blocks or text blocks.
    """

    document = Document(value)

    blocks = flatten([selector(block) for block in document.children])
    return [block for block in blocks if block is not None]
