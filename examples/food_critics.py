"""
Ask a panel of food critics to rate a list of entreés.
"""

from os import environ

from langchain_community.chat_models import ChatOllama

from packit.agent import Agent
from packit.formats import format_bullet_list
from packit.panel import Panel

# Inputs
backstories = {
    "harsh": "You are a harsh food critic. You are rating a list of entreés, harshly.",
    "average": "You are an average food critic. You are rating a list of entreés, averagely.",
    "generous": "You are a generous food critic. You are rating a list of entreés, generously.",
}

entrees = [
    "spaghetti carbonara",
    "pad thai",
    "chicken tikka masala",
    "beef bourguignon",
    "sushi",
    "pizza",
    "hamburger",
    "hot dog",
    "tacos",
    "ramen",
    "pho",
]

prompts = {
    "entree": "Do you think {entree} is a good dish? Reply with a one word answer, yes or no.",
}

decisions = {
    True: "good",
    False: "bad",
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

# Create the food critics
critics = {
    critic: Agent(f"{critic} critic", backstory, {}, llm)
    for critic, backstory in backstories.items()
}

# Create the panel, but make sure we listen to the generous critic twice as much
panel_weights = {
    critics["harsh"]: 1,
    critics["average"]: 1,
    critics["generous"]: 2,
}
panel = Panel(panel_weights)

# Rate each of the entreés
for entree in entrees:
    decision, reasons = panel(prompts["entree"], entree=entree)
    print(
        f"The critics decided that {entree} is {decisions[decision]} because:\n{format_bullet_list(reasons.values())}"
    )
