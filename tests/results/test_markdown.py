from unittest import TestCase

from packit.results import markdown_result, select_text_blocks


class TestMarkdown(TestCase):
    def test_markdown_code(self):
        # Markdown document
        markdown = """
# Markdown Example

## Code Block

```python
print("Hello, World!")
```

## Text Block

This is a text block.
        """

        # Parse markdown and return code blocks
        code_blocks = markdown_result(markdown)
        self.assertEqual(
            code_blocks,
            [
                'print("Hello, World!")',
            ],
        )

    def test_markdown_text(self):
        # Markdown document
        markdown = """
# Markdown Example

## Text Block

This is a text block."""

        # Parse markdown and return text blocks
        text_blocks = markdown_result(markdown, selector=select_text_blocks)
        self.assertEqual(
            text_blocks,
            [
                "This is a text block.",
            ],
        )


if __name__ == "__main__":
    from unittest import main

    main()
