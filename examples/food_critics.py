"""
Ask a panel of food critics to rate a list of entreés.
"""

from packit.agent import Agent, agent_easy_connect
from packit.formats import format_bullet_list
from packit.groups import Panel
from packit.tracing import trace
from packit.utils import logger_with_colors

logger = logger_with_colors(__name__)

# Inputs
backstories = {
    "harsh": "You are a harsh food critic. You are rating a list of entreés, harshly.",
    "average": "You are an average food critic. You are rating a list of entreés, averagely.",
    "generous": "You are a generous food critic. You are rating a list of entreés, generously.",
    "unpredictable": "You are an unpredictable food critic. You are rating a list of entreés, unpredictably.",
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

decisions = {
    True: "good",
    False: "bad",
}

# Create the food critics
llm = agent_easy_connect(model="mixtral")
critics = [
    Agent(f"{critic} critic", backstory, {}, llm)
    for critic, backstory in backstories.items()
]

# Create the panel, but make sure we listen to the generous critic twice as much
critic_weights = [1, 1, 2, 1]
panel = Panel(critics, name="food_critics", weights=critic_weights)

# Rate each of the entreés
for entree in entrees:
    with trace("task", "packit.example") as (report_args, report_output):
        report_args(entree)

        decision, reasons = panel(
            "Do you think {entree} is a good dish? Reply with a one word answer, yes or no.",
            entree=entree,
        )

        report_output(decision)
        logger.info(
            f"The critics decided that {entree} is {decisions[decision]} because:\n{format_bullet_list(reasons.values())}"
        )
