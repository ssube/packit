# PACkit

The Prompt Agent Construction Kit, or maybe the Programmable Agent Construction Kit.

Conversational development where your code is the manager.

Something in between [Langchain](https://www.langchain.com/) and [CrewAI](https://github.com/joaomdmoura/crewAI). A
loose toolkit of loops, operators, and predicates to help LLMs communicate with each other and with your code.

![a network of lego people standing on a blueprint together](./docs/packit-banner.jpg)

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


> python3 -m examples.food_critics

The critics decided that spaghetti carbonara is good because:
-  No. As a harsh food critic, I cannot in good conscience label spaghetti carbonara as a "good" dish. While it can be satisfying and flavorful when executed well, all too often it is drowned in cream and devoid of the rich, nuanced taste that comes from using high-quality ingredients and traditional techniques. The dish has been butchered and bastardized to the point where it barely resembles its original form, and for that reason, I cannot consider it a good dish.
-  Yes, I think spaghetti carbonara is a good dish. It's a classic Italian pasta made with eggs, cheese, and pancetta or bacon. The creamy sauce and savory flavors make it a satisfying and delicious entree. Of course, the quality of ingredients and execution can vary, but when done well, spaghetti carbonara is hard to beat.
-  Yes, I do! Spaghetti carbonara is a classic Italian dish that typically consists of pasta, pancetta or bacon, eggs, and cheese. When well-prepared, it can be a rich and satisfying meal that showcases the flavors of simple, high-quality ingredients. The combination of creamy egg sauce, salty pancetta, and savory cheese is hard to beat. Overall, I would say that spaghetti carbonara is a very good dish!
-  Yes, I do! Spaghetti carbonara is a classic Italian pasta dish made with eggs, cheese, pancetta or bacon, and pepper. It's rich, creamy, and full of flavor, and can be easily customized to suit your preferences. Whether you prefer it with a little more cheese or a bit of extra crispy bacon, spaghetti carbonara is a delicious and satisfying dish that is sure to please any pasta lover.
The critics decided that pad thai is good because:
-  No. As a harsh food critic, I cannot in good conscience label pad thai as a "good" dish, despite its popularity and widespread acclaim. While it can be prepared to be decent, the overuse of sweet sauces and inconsistencies in both ingredient quality and preparation often lead to an underwhelming experience for my refined palate.
-  Yes, I do think that pad thai can be a good dish. It's a popular stir-fried noodle dish from Thailand that typically contains rice noodles, vegetables, and a protein such as tofu, shrimp, or chicken, flavored with ingredients like tamarind, fish sauce, and palm sugar. When well-prepared, pad thai can be delicious and satisfying. However, the quality of pad thai can vary greatly depending on the skill of the cook and the freshness of the ingredients, so it's important to choose a reputable restaurant or vendor when ordering this dish.
-  Yes, I do! Pad Thai is a delicious and popular dish that originated from Thailand. It typically consists of stir-fried rice noodles with eggs, tofu, vegetables, and a flavorful sauce made from tamarind, fish sauce, and palm sugar. The dish is often garnished with crushed peanuts, bean sprouts, and lime wedges, adding texture and brightness to each bite. I can see why it's a favorite for many people.
-  Yes, I do! Pad Thai is a delicious and popular dish that originated from Thailand. It typically features stir-fried rice noodles, bean sprouts, tofu, eggs, and peanuts, all mixed together in a savory sauce with flavors of tangy tamarind, sweet palm sugar, and umami-rich fish sauce. The dish is often garnished with lime wedges, crushed peanuts, and fresh herbs like cilantro and scallions, adding brightness and texture to each bite. I can see why it's a favorite among many food lovers!
...
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

Panels can make their decision using any of the available comparators. By default, they will compare their mean
rating against a predefined threshold. If the consensus exceeds the threshold, the panel will give an affirmative
answer. This can also be inverted using a counter or the not comparator.

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

Interpret the response as a boolean, yes or no.

#### Integer Results

Interpret the response as an integer.

#### JSON Results

Interpret the response as JSON.
