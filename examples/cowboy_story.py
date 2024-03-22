"""
N cowboys are sitting around a fire, each telling part of an ever-growing story.
"""

from os import environ
from random import choice, randint

from langchain_community.chat_models import ChatOllama

from packit.agent import Agent
from packit.loops import loop_refine

# Inputs
backstories = [
    "You are a cowboy sitting around a campfire. You are telling a story.",
]

prompts = {
    "start": "You are a cowboy sitting around a campfire. You are telling a story.",
}

# Connect to a local LLM
ollama_api = environ.get("OLLAMA_API", "http://localhost:11434")
ollama_model = environ.get("OLLAMA_MODEL", "mixtral")
num_ctx = environ.get("OLLAMA_NUM_CTX", 2048)
num_gpu = environ.get("OLLAMA_NUM_GPU", 20)

llm = ChatOllama(
    temperature=0.65,
    model=ollama_model,
    base_url=ollama_api,
    num_ctx=num_ctx,
    num_gpu=num_gpu,
)

# Create the cowboys
cowboy_count = randint(3, 6)
cowboys = [
    Agent(f"cowboy {i}", choice(backstories), {}, llm) for i in range(cowboy_count)
]

# Choose a random cowboy to start the story
starter = choice(cowboys)
story = starter(prompts["start"])

# Each cowboy tells a part of the story
story = loop_refine(cowboys, story)

# Print the story
print(story)
