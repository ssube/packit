# PACkit

Prompt Agent Construction Kit.

Something in between Langchain and CrewAI. Conversational development where your code is the manager.

## Contents

- [PACkit](#packit)
  - [Contents](#contents)
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
