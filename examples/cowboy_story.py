"""
N cowboys are sitting around a fire, each telling part of an ever-growing story.
"""

from random import choice, randint

from packit.agent import Agent, agent_easy_connect
from packit.loops.legacy import loop_extend
from packit.utils import logger_with_colors

logger = logger_with_colors(__name__)

# Inputs
backstories = [
    "You are a cowboy sitting around a campfire, telling an increasingly unbelievable story.",
]

prompts = {
    "start": "Start a campfire story about ghostly porcupines.",
}

# Create the cowboys
llm = agent_easy_connect(model="mixtral")
cowboy_count = randint(3, 6)
cowboys = [
    Agent(f"cowboy {i}", choice(backstories), {}, llm) for i in range(cowboy_count)
]

# Choose a random cowboy to start the story
starter = choice(cowboys)
story = starter(prompts["start"])

# Each cowboy tells a part of the story
story = loop_extend(cowboys, story)

# Print the story
logger.info(story)
