from random import choice

from langchain_openai import ChatOpenAI

from packit.agent import Agent
from packit.loops import loop_converse

llm = ChatOpenAI(model="gpt-4", temperature=0)

ending = "Leave the end open for the next person to continue the story."
backstories = {
    "captain": "You are a ship's captain, telling a story of the one that didn't get away. "
    + ending,
    "fisherman": "You are a fisherman, recounting a tale of the one that got away. "
    + ending,
    "pirate": "You are a salty pirate, telling a tale of the high seas. " + ending,
    "sailor": "You are a sailor, spinning a yarn about the open ocean. " + ending,
}

agents = [Agent(name, backstory, {}, llm) for name, backstory in backstories.items()]
starter = choice(agents)

story = starter("Start writing a tall tale about sea monsters.")
story = loop_converse(agents, story)

print("The tall tale is:", story)
