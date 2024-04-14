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
      - [Key Components of the Agent](#key-components-of-the-agent)
      - [Importance of the System Prompt](#importance-of-the-system-prompt)
      - [Customizing Model Behavior](#customizing-model-behavior)
      - [LLM Temperature](#llm-temperature)
    - [Prompt](#prompt)
    - [Context](#context)
    - [Toolbox](#toolbox)
      - [Restricted Toolbox](#restricted-toolbox)
  - [Loops Constructs](#loops-constructs)
    - [Basic Loops](#basic-loops)
      - [Map](#map)
        - [Map Example](#map-example)
      - [Reduce](#reduce)
        - [Reduce Example](#reduce-example)
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

The basic Agent in PACkit is a fundamental component designed to manage interactions with language model agents (LLMs).
This entity encapsulates the core attributes and functionalities needed to interface effectively with sophisticated AI
models, facilitating targeted conversations and decision-making processes.

```python
from packit import Agent
from langchain.openai import OpenAIChat

# Setup the OpenAI chat model from Langchain
# Assume API_KEY is your OpenAI API key; this should be securely managed
api_key = "your_openai_api_key"
chat_model = OpenAIChat(api_key=api_key, model="gpt-4")  # Using GPT-4 for this example

# Define the backstory and context for the agent
backstory = "I am a travel advisor bot trained to provide travel advice, " \
            "including destinations, booking tips, and current travel safety measures."
context = {
    "travel_trends": "current",
    "health_safety_standards": "updated",
    "preferred_destinations": "tropical islands"
}

# Create the agent with the specified Langchain model
travel_advisor_agent = Agent(
    name="TravelAdvisor",
    backstory=backstory,
    context=context,
    llm=chat_model
)

# Now you can use this agent to handle prompts relevant to its domain
prompt = "What are the top three destinations for a family vacation in July?"
response = travel_advisor_agent.llm.chat(prompt=prompt)

print("Travel Advice:", response)
```

#### Key Components of the Agent

- **Name**: This is a short identifier or codename for each agent, helping to distinguish between different agents within
  the system. The name typically reflects the agent's specialty or primary function.
- **Backstory**: The backstory of an agent serves as the system prompt for the LLM used by that agent. This is a crucial
  component as it sets the initial context or "personality" of the agent. It provides foundational knowledge and
  instructions that influence how the agent interprets and responds to prompts.
- **Context**: This is a dictionary containing specific facts or key pieces of information that the agent knows and can
  utilize in its reasoning and responses. The context enhances the agent's ability to provide relevant and accurate
  information tailored to the situation at hand.
- **LLM**: This parameter links the agent to a specific language model. The choice of LLM influences the agent's
  capabilities, as different models may be trained on different data sets or optimized for different types of tasks.

#### Importance of the System Prompt

The system prompt, encapsulated in the agent's backstory, is essential in shaping the behavior of the LLM. By providing
a narrative or a set of instructions embedded within the backstory, developers can guide the LLM's responses to align
with specific objectives or operational guidelines. This can include emphasizing certain types of information, adhering
to regulatory requirements, or avoiding particular topics. The backstory effectively primes the LLM, setting the stage
for its interactions and ensuring consistency in its approach to handling queries.

#### Customizing Model Behavior

Customization of an LLM's behavior is primarily achieved through the backstory and context parameters. By adjusting
these elements, developers can fine-tune how the model processes and responds to input:

- **Backstory Adjustments**: Modifying the backstory can change the model's focus, ethical guidelines, or knowledge base,
  directly influencing how it interprets and responds to prompts.
- **Contextual Tweaks**: By updating the context dictionary, developers can provide the agent with up-to-date information,
  specialized knowledge, or situational awareness, enhancing the relevance and accuracy of its responses.

#### LLM Temperature

The temperature setting for an LLM is an important parameter that controls the randomness of the model's responses.
While not detailed here, it's worth noting that adjusting the temperature can affect the creativity and variability of
the agent's output. Lower temperatures generally result in more predictable and conservative responses, whereas higher
temperatures may produce more diverse and less deterministic outputs.

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

The `loop_map` function in PACkit is an embodiment of the functional programming paradigm `map`, adapted for
orchestrating operations across one or more language model agents (LLMs). This construct applies a given prompt to an
array of agents, each potentially tailored with specialized capabilities, and aggregates their independent outputs into
a list. The signature for `loop_map` includes parameters for the agents, the prompt, and an optional context, which
enriches the environment in which each agent operates, enhancing the pertinence and depth of their responses.
Importantly, `loop_map` retains an internal history of interactions, leveraging the same memory mechanisms utilized by
agents for maintaining state across sessions. This feature is critical in applications where continuity of context
enhances the quality of the decision-making process, such as in iterative refinement tasks or multi-agent consultations
within the AI/ML domain.

![map diagram](./packit-map.png)

##### Map Example

This example demonstrates how to use `loop_map` to concurrently send a prompt to a list of agents. Each agent will
respond independently, and the responses will be aggregated into a list.

```python
from packit import Agent, loop_map

# Define some mock agents with different areas of expertise
agent1 = Agent(name="DataScientist", backstory="Expert in data analysis", context={}, llm="Langchain Data Model")
agent2 = Agent(name="MLExpert", backstory="Specializes in machine learning algorithms", context={}, llm="Langchain ML Model")

# Define a list of agents
agents = [agent1, agent2]

# Define a prompt to send to all agents
prompt = "What are the latest trends in your field?"

# Execute the map loop
responses = loop_map(agents=agents, prompt=prompt)

# Print each agent's response
for response in responses:
    print(response)
```

In this example, `loop_map` sends the same prompt to two different agents, each specializing in different aspects of AI
and machine learning. The function collects responses from each agent and returns them as a list.

#### Reduce

This loop passes the result of one agent as a prompt to the next, effectively creating a chain of responses that refine
or expand upon the initial input.

Conversely, the `loop_reduce` function represents a sophisticated implementation of the `reduce` (or `fold`) operation
from functional programming, specifically tailored for sequential data processing tasks in machine learning and AI
contexts. This function iteratively applies a prompt to a sequence of agents, where the output from one agent serves as
the input to the next, thereby chaining their responses to evolve the prompt dynamically. The `loop_reduce` function
accepts either a single agent or a list of agents, a prompt, and an optional context, which may modify the agent's
operational parameters or influence its output. The operation concludes with a single consolidated result from the final
agent in the sequence, embodying the cumulative modifications imposed by all preceding agents. Similar to `loop_map`,
`loop_reduce` also maintains an internal history of the prompt’s evolution across agents using the same memory
mechanisms inherent to the agents. This feature is invaluable for tasks requiring progressive elaboration or refinement,
such as generating complex reports, developing ideas, or troubleshooting where each step builds upon the previous one in
a logical and coherent manner.

![reduce diagram](./packit-reduce.png)

##### Reduce Example

This example shows how to use `loop_reduce` to pass a prompt through a series of agents, where each agent processes the
prompt and passes its output to the next agent. The final output is the result of the cumulative processing by all
agents.

```python
from packit import Agent, loop_reduce

# Define some mock agents that will process information in a sequential manner
agent1 = Agent(name="Researcher", backstory="Identifies key issues", context={}, llm="Langchain Research Model")
agent2 = Agent(name="Analyst", backstory="Analyzes identified issues", context={}, llm="Langchain Analysis Model")
agent3 = Agent(name="SolutionArchitect", backstory="Proposes solutions based on analysis", context={}, llm="Langchain Solution Model")

# Define a list of agents
agents = [agent1, agent2, agent3]

# Define an initial prompt
initial_prompt = "Examine the impact of AI on urban sustainability."

# Execute the reduce loop
final_result = loop_reduce(agents=agents, prompt=initial_prompt)

# Print the final result
print(final_result)
```

In this `loop_reduce` example, the prompt starts with the first agent who examines a broad topic, the next agent analyzes
the issues identified by the first, and finally, the third agent proposes solutions based on the analysis. The output
from each agent serves as the input for the next, resulting in a comprehensive final result that encapsulates the input
and work of all agents involved.

### Single-agent Loops

#### Retry

The `loop_retry` construct in PACkit serves as an iterative error-correction mechanism, enhancing the robustness of
interactions with language model agents (LLMs). At its core, the `loop_retry` function encapsulates a feedback loop
where an agent's response is evaluated for correctness and completeness based on a defined result parser. If the parser
encounters an error, indicating that the response is not satisfactory, the prompt is modified, usually by appending an
error message or clarification, and re-presented to the agent for another attempt.

![retry diagram](./packit-retry.png)

The function signature for the `loop_retry` is as follows:

```python
def loop_retry(
    agents: Agent | list[Agent],
    prompt: PromptType,
    context: AgentContext | None = None,
    result_parser: ResultParser,
) -> PromptType:
    ...
```

The retry loop is optimally utilized with a single agent, which underpins its primary use case: refining the output of
an LLM until the result meets the specified criteria. The process begins with the agent receiving an initial prompt,
followed by a response that is then passed through the result parser. If the parser detects an error—such as an
incomplete answer, a logical inconsistency, or information that does not match the required format—the error is fed back
into the loop. The prompt, now augmented with additional information derived from the parser's error, is presented
again, and the agent is prompted to rectify the mistake.

This iterative process continues until the result parser successfully validates a response or until a predefined stop
condition is met, typically a maximum number of iterations. This stop condition is crucial as it prevents an indefinite
loop in the event that the agent is incapable of generating a valid response.

In more complex scenarios involving multiple agents, the `loop_retry` can be extended to engage secondary agents for
assistance. Should the primary agent fail to provide a valid response, subsequent agents can be invoked to attempt to
repair the output. This collaborative approach can enhance the likelihood of achieving a valid result, leveraging the
collective capabilities of multiple LLMs.

The `loop_retry` loop, depicted in the provided diagram, clearly illustrates this process with a flow of steps:
beginning with the initial prompt, proceeding through the error-checking phases, and culminating in either a successful
result or an error-based loop iteration. This visual representation serves as an intuitive guide to understanding the
loop's mechanisms and its practical applications within PACkit.

Here is a hypothetical code snippet using `loop_retry`:

```python
from packit import Agent, loop_retry, ResultParser

# Define a single agent with its properties
agent = Agent(
    name="QAAssistant",
    backstory="A quality assurance assistant that validates information accuracy.",
    context={"valid_data_sources": "trusted_datasets"},
    llm="Langchain QA Model"
)

# Define the prompt to be sent to the agent
prompt = "Verify the accuracy of the following data: [data snippet]"

# Define a result parser that checks the response for accuracy
def result_parser(response):
    # Pseudo-code for parsing the result
    if "error" in response or "unverified" in response:
        return None, "Error: The data could not be verified. Please try again."
    else:
        return response, None

# Execute the retry loop with the agent
final_result = loop_retry(
    agents=agent,
    prompt=prompt,
    result_parser=result_parser
)

print(final_result)
```

In this code example, the loop_retry function is employed to ensure that the QA assistant agent provides a response that
passes the verification criteria set by the result_parser. If the parser identifies an issue, the agent is prompted to
revise its response until it is deemed accurate or until the retry attempts are exhausted.

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
