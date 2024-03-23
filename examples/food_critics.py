"""
Ask a panel of food critics to rate a list of entreés.
"""

from packit.agent import Agent, agent_easy_connect
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
    "dirt",
    "rocks",
    "batteries",
    "a shoe",
    "noodles",
    "rice",
]

prompts = {
    "entree": "Do you think {entree} is a good dish? Reply with a one word answer, yes or no.",
}

decisions = {
    True: "good",
    False: "bad",
}

# Create the food critics
llm = agent_easy_connect()
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
