from unittest import TestCase

from packit.results import markdown_result


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

This is a text block.
        """

        # Parse markdown and return text blocks
        text_blocks = markdown_result(markdown, block_type="text")
        self.assertEqual(
            text_blocks,
            [
                "This is a text block.",
            ],
        )


if __name__ == "__main__":
    test = TestMarkdown()
    test.test_markdown()
    print("Test passed")
