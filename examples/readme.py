from random import choice

from packit.agent import Agent, agent_easy_connect
from packit.loops import loop_converse
from packit.utils import logger_with_colors

logger = logger_with_colors(__name__)

ending = "Leave the end open for the next person to continue the story."
backstories = {
    "captain": "You are a ship's captain, telling a story of the one that didn't get away. "
    + ending,
    "fisherman": "You are a fisherman, recounting a tale of the one that got away. "
    + ending,
    "pirate": "You are a salty pirate, telling a tale of the high seas. " + ending,
    "sailor": "You are a sailor, spinning a yarn about the open ocean. " + ending,
}

llm = agent_easy_connect(model="mixtral")
agents = [Agent(name, backstory, {}, llm) for name, backstory in backstories.items()]
starter = choice(agents)

story = starter("Start writing a tall tale about sea monsters.")
story = loop_converse(agents, story)

logger.info("The tall tale is:", story)
