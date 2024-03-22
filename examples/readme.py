from random import choice

from langchain_openai import ChatOpenAI

from packit.agent import Agent
from packit.loops import loop_converse

llm = ChatOpenAI(model="gpt-4", temperature=0)

backstories = {
    "captain": "You are a ship's captain, telling a story of the one that didn't get away.",
    "fisherman": "You are a fisherman, recounting a tale of the one that got away.",
    "pirate": "You are a salty pirate, telling a tale of the high seas.",
    "sailor": "You are a sailor, spinning a yarn about the open ocean.",
}

agents = {k: Agent(v, backstories[k], {}, llm) for k, v in backstories.items()}
starter = choice(list(agents.values()))

story = starter("Start writing a tall tale about sea monsters.")
story = loop_converse(agents, story)

print("The tall tale is:", story)
