# PACkit

Prompt Agent Construction Kit.

Conversational development where your code is the manager.

Something in between [Langchain](https://www.langchain.com/) and [CrewAI](https://github.com/joaomdmoura/crewAI). A
loose toolkit of loops, operators, and predicates to help LLMs communicate with code.

## Contents

- [PACkit](#packit)
  - [Contents](#contents)
  - [Examples](#examples)
    - [With OpenAI API](#with-openai-api)
    - [With Local Ollama](#with-local-ollama)
  - [Concepts](#concepts)
    - [Agents](#agents)
      - [Agent Backstory](#agent-backstory)
      - [Agent Context](#agent-context)
      - [Agent Temperature](#agent-temperature)
    - [Panels](#panels)
      - [Panel Methods](#panel-methods)
      - [Panel Results](#panel-results)
    - [Loops](#loops)
      - [Conversation Loops](#conversation-loops)
      - [Panel Loops](#panel-loops)
      - [Refinement Loops](#refinement-loops)
    - [Results](#results)
      - [Binary Results](#binary-results)
      - [Integer Results](#integer-results)
      - [JSON Results](#json-results)

## Examples

### With OpenAI API

TODO: OpenAI example

### With Local Ollama

Launch a local [Ollama server](https://ollama.com/) with the [Mixtral model](https://mistral.ai/news/mixtral-of-experts/):

```shell
export OLLAMA_HOST=0.0.0.0 # only needed for remote access
export OLLAMA_MODELS=/mnt/very-large-disk/ollama/models

ollama pull mixtral
ollama serve
```

Run the examples:

```shell
> python3 -m examples.cowboy_story
 Gather 'round folks, and listen close as I recount the tale of a legendary haunted cattle drive. It was a dark and stormy night, not unlike this one, when a group of hardened cowboys set out to drive a herd of cattle from Texas to Kansas.

These cowboys were some of the toughest hombres around; they had faced danger many times before and lived to tell the tale. Yet, they had heard whispers of strange occurrences along this very trail. They dismissed it as mere superstition and embarked on their journey.

As they made their way northward, they began to notice peculiar happenings. Cattle would low in fear for no apparent reason, and the horses became easily spooked. At night, eerie howls and moans echoed around them, seeming to come from nowhere and everywhere at once.

One evening, as they sat by their campfire, much like we are now, a lone figure approached riding towards them. As it drew nearer, they discerned it was a cowboy, his face pale and drawn. He rode up to the fire and cautioned them about the haunted cattle drive.

"I was part of a group that attempted to drive these cattle before," he said, "but we were plagued by uncanny happenings. Cattle would vanish without a trace during the night, only to be discovered miles away, lifeless and drained of blood. Horses would suddenly rear and buck without provocation. And when darkness fell, we'd hear shrill screams and wails emanating from what sounded like the very earth itself."

The cowboys scoffed at his warning, insisting they weren't afraid of any ghost stories. However, as days turned into nights, more inexplicable events transpired. Though they couldn't understand why, they knew something was amiss.

One night, while they lay asleep under the stars, a blood-curdling scream pierced the silence. They grabbed their guns and rushed out into the darkness, where they saw a ghostly figure riding towards them. It was a woman, dressed all in white, her face contorted in a scream of terror.

The cowboys watched as she rode past them, right through their campfire, leaving behind nothing but smoke and ash. Her chilling screams lingered in their ears long after she disappeared into the shadowy night.

From that moment forth, they believed in the legend. They hurried their cattle to Kansas, never stopping or looking back. When they finally arrived, relief washed over them, but they never forgot the haunted cattle drive.

So, as you sit around this campfire, listening to my tale, remember the legend of the Haunted Cattle Drive. Out here on the prairie, one can never truly know what might be lurking in the shadows.
```

## Concepts

### Agents

An `Agent` is a particular configuration of an LLM with a backstory, facts, and temperature.

#### Agent Backstory

An `Agent`'s backstory defines who they are and how they will behave.

In technical terms, the backstory is the system prompt, which influences what role the LLM takes when responding.

#### Agent Context

An `Agent`'s context are the facts they will always know.

In technical terms, the context is the dictionary of variables available for use in template strings.

#### Agent Temperature

An `Agent`'s temperature controls how creative they will be, but too high of a temperature will stop making sense.

### Panels

A `Panel` is a weighted panel of agents. Each agent will be given the same user prompt, along with their own system
prompt, or backstory. Their responses will be interpreted the same way. Agents with a greater weight will be asked more
often than the others.

#### Panel Methods

Panels can use many methods to make their decision. Agents can respond with a yes/no answer or rank items on a scale.
When multiple items are provided, they can be evaluated individually or as a single group (with a large enough
context window).

#### Panel Results

Panels can make their decision using

### Loops

#### Conversation Loops

Using two or more agents, have them respond to one another in a conversational manner.

The conversation will continue until the iteration limit has been reached or the stop condition becomes true.

This is similar to what CrewAI does, but much simpler.

#### Panel Loops

[Panels](#panels) are another kind of loop.

#### Refinement Loops

Using one or more agents, have them incrementally refine the output.

The refinement will continue until the iteration limit has been reached or the stop condition becomes true.

### Results

#### Binary Results

Interpret the response as an integer.

#### Integer Results

Interpret the response as an integer.

#### JSON Results

Interpret the response as JSON.
