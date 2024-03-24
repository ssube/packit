# Notes

These are some miscellaneous notes about the PACkit project and code.

## Contents

- [Notes](#notes)
  - [Contents](#contents)
  - [Duplication with Langchain](#duplication-with-langchain)
  - [Examples](#examples)
  - [Composability](#composability)

## Duplication with Langchain

There are some constructs that are very similar to constructs in Langchain and some redundancy there.

Those exist for one (or sometimes both) of two reasons:

- the API is different and offers more control
- I don't know what I'm doing and am not familiar with that feature in Langchain

## Examples

- Examples should run on their own, as standalone Python scripts
- Examples should be compatible with both OpenAI and Ollama
- Examples should be < 100 lines of code
- Examples should not need to import directly from `langchain*`

## Composability

- Components must not use global state, othere than the default prompts
- Components with internal state must provide a way to reset that state
