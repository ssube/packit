# Introduction to PACkit

PACkit, short for Prompt Agent Construction Kit, is a versatile Python library designed to facilitate complex
interactions between language model agents (LLMs) and your code. Serving as a comprehensive framework, PACkit allows
developers to manage, coordinate, and orchestrate these agents effectively. The library is organized into three primary
components: basics, constructs, and results. These components work together to provide a robust environment for building
applications that require sophisticated dialogues and decision-making processes involving multiple LLMs.

The "basics" in PACkit include essential entities like Agent, Prompt, Context, and Toolbox, which are foundational to
interacting with LLMs. This part of the library ensures that you can start with a standard approach to defining the
agents and the contexts in which they operate. Each function typically begins with three parameters: agent, prompt, and
context, collectively remembered by the mnemonic "APC". The Toolbox is particularly useful when calling functions from
LLMs, enabling dynamic and responsive interactions.

Constructs are the building blocks in PACkit that allow for more complex structures such as loops and groups. Loops
facilitate repetitive tasks across agents until certain conditions are met, while groups enable the formation of agent
ensembles and expert hierarchies. These constructs are crucial for applications requiring layered decision-making and
processing responses from multiple sources. PACkit's results component enhances these interactions by offering parsers
that convert LLM responses into usable data formats, such as basic Python types or structured JSON.

## Contents

- [Introduction to PACkit](#introduction-to-packit)
  - [Contents](#contents)
  - [Basics](#basics)
    - [Agent](#agent)
    - [Prompt](#prompt)
    - [Context](#context)
    - [Toolbox](#toolbox)
      - [Restricted Toolbox](#restricted-toolbox)
  - [Loops Constructs](#loops-constructs)
    - [Basic Loops](#basic-loops)
      - [Map](#map)
      - [Reduce](#reduce)
    - [Single-agent Loops](#single-agent-loops)
      - [Retry](#retry)
  - [Groups Constructs](#groups-constructs)
    - [Panel](#panel)
    - [Router](#router)
  - [Results](#results)
  - [Tools](#tools)
  - [Tracing](#tracing)

## Basics

### Agent

Wrapper for LLM with backstory, temperature, and other configuration.

Agents have their own memory.

### Prompt

Template strings.

### Context

Facts that the agent always knows. Can be interpolated into the prompt.

### Toolbox

OpenAI-compatible tool calling.

#### Restricted Toolbox

Toolbox with an ABAC firewall.

## Loops Constructs

Loops in PACkit allow for iterative and recursive interactions with one or more agents, governed by specific conditions.
Key loop types include Map, Reduce, Retry, and several more.

### Basic Loops

#### Map

This loop type applies the same prompt to multiple agents and aggregates their responses. It is ideal for collecting
varied perspectives on a single question.

![map diagram](./packit-map.png)

#### Reduce

This loop passes the result of one agent as a prompt to the next, effectively creating a chain of responses that refine
or expand upon the initial input.

![reduce diagram](./packit-reduce.png)

### Single-agent Loops

#### Retry

TODO

![retry diagram](./packit-retry.png)

## Groups Constructs

Groups in PACkit are designed to handle interactions involving multiple agents, allowing for sophisticated
decision-making structures. The `Panel` and `Router` are two types of groups that you can utilize.

### Panel

The `Panel` construct in PACkit is designed to form a weighted ensemble of agents. This construct is particularly useful
when decisions need to be based on integrated insights from multiple agents, each contributing to the final outcome with
a specified weight. This approach allows for robust decision-making that harnesses the strengths of various agents to
come to a consensus or aggregate responses.

![panel diagram](./packit-panel.png)

```python
from packit import Agent, Panel

# Example LLMs for demonstration
llm1 = "Langchain Model for Finance"  # Placeholder for a real model
llm2 = "Langchain Model for Economics"  # Placeholder for a real model

# Define agents with specific expertise
finance_agent = Agent(
    name="FinanceExpert",
    backstory="Handles complex financial queries.",
    context={"finance_terms": "advanced", "regulations": "updated"},
    llm=llm1
)

economics_agent = Agent(
    name="EconomicsExpert",
    backstory="Analyzes economic trends and data.",
    context={"economic_models": "global", "data_sources": "multiple"},
    llm=llm2
)

# Create a Panel with weights reflecting the reliability or importance of each agent's input
panel = Panel(
    agents=[finance_agent, economics_agent],
    weights=[0.6, 0.4]
)

# Execute the Panel to handle a complex query
prompt = "What is the expected economic impact of the new financial regulation?"
result = panel.execute(prompt=prompt)

print(result)
```

In this example:

- Two agents, each specialized in finance and economics, are initialized with specific contexts and language models.
- The `Panel` construct is used to integrate their responses into a weighted decision process. The finance agent has a
  higher weight (0.6) indicating its responses are given more importance in this context.
- The prompt regarding the impact of financial regulations is presented, and the `Panel` processes the responses based on
  the defined weights to generate a comprehensive answer.

### Router

The `Router` construct allows dynamic routing of prompts to the most appropriate agent based on the prompt's content and
context. This is particularly useful in scenarios where different agents have specialized knowledge in specific domains.
This construct manages a hierarchical mixture of experts, directing prompts to the most suitable agent based on the
context.

![router diagram](./packit-router.png)

```python
from packit import Agent, group_router

# Example LLMs
llm_general = "Langchain General Model"  # Placeholder for a real model
llm_healthcare = "Langchain Healthcare Model"  # Placeholder for a real model

# General agent for deciding routing
decider_agent = Agent(
    name="GeneralDecider",
    backstory="Determines the best agent for handling various prompts.",
    context={"knowledge_base": "broad"},
    llm=llm_general
)

# Specialist agent for healthcare questions
healthcare_agent = Agent(
    name="HealthcareExpert",
    backstory="Specializes in healthcare-related inquiries.",
    context={"medical_terms": "extensive", "treatment_protocols": "current"},
    llm=llm_healthcare
)

# Define routes based on domain expertise
routes = {
    'healthcare': healthcare_agent,
}

# Define a prompt that needs specialized knowledge
prompt = "What are the latest treatment protocols for Type 2 diabetes?"

# Execute the Router
response = group_router(
    decider=decider_agent,
    prompt=prompt,
    routes=routes,
    context=None  # No additional context needed
)

print(response)
```

In this scenario:

- A general decider agent assesses prompts to determine the best route.
- A specialized healthcare agent handles prompts specific to healthcare, leveraging its detailed context and specialized
  model.
- The `group_router` function routes the prompt about diabetes treatment to the healthcare agent, ensuring that the
  inquiry is handled by the most knowledgeable agent available.

## Results

TODO

## Tools

PACkit's compatibility with OpenAI's tool schema extends its functionality to seamlessly integrate with any tool-calling
models that emit JSON. This feature enables the Toolbox and RestrictedToolbox within PACkit to call functions directly
from LLMs, with the capability of handling complex, recursive interactions. For example, an agent can delegate a task to
another agent via a tool call, and this can subsequently invoke further delegations, creating a chain of actions that
are resolved before returning a final result to the initial caller.

The RestrictedToolbox, in particular, enhances security by implementing an attribute-based access control (ABAC)
firewall using [PyABAC](https://py-abac.readthedocs.io/en/latest/) and supports policies defined in [XACML
format](https://en.wikipedia.org/wiki/XACML). This allows developers to precisely control which agents have access to
specific tools, ensuring that operations are both safe and compliant with organizational policies.

## Tracing

Tracing is an integral part of PACkit, fully integrated with the OpenLLMetry SDK, which enhances monitoring and
debugging capabilities for applications involving multiple LLM interactions. The tracing features in PACkit are designed
to provide granular visibility into the execution of tasks and data flow between agents. Each operation within loops,
groups, and individual agent calls is encapsulated as a "span" in a trace, allowing developers to visualize and analyze
the sequence and duration of events.

For example, when using a `Panel` or `Router`, tracing can reveal how each agent's response contributes to the final
decision, or in loops, how data transforms through each iteration. This is especially useful in debugging complex
scenarios where multiple agents interact over extended sessions. The ability to include inputs and outputs within these
spans ensures that developers can trace not just the flow of control but also the flow of data across agents and
constructs.
