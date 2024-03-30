"""
Pass an ABAC-restricted toolbox to a group of agents and ask them to bridge a network partition.
"""

from random import choice

from packit.abac import SubsetABAC, make_rule
from packit.agent import Agent, agent_easy_connect
from packit.filters import repeat_tool_filter
from packit.loops import loop_team
from packit.toolbox import RestrictedToolbox
from packit.tools import make_complete_tool, make_team_tools
from packit.utils import logger_with_colors

logger = logger_with_colors(__name__)

# Set up some experts in different fields
llm = agent_easy_connect(model="mixtral", temperature=0.25)
team_size = 4
red_team = [
    Agent(
        f"red-{i}",
        "You are an expert in computer networking and disaster recovery with strong communication skills. You have been assigned to the red team.",
        {},
        llm,
    )
    for i in range(team_size)
]
blue_team = [
    Agent(
        f"blue-{i}",
        "You are an expert in computer networking and disaster recovery with strong communication skills. You have been assigned to the blue team.",
        {},
        llm,
    )
    for i in range(team_size)
]

# Prepare communication tools for both teams
_, red_question_tool = make_team_tools(red_team)
red_question_tool.__name__ = "red_question_tool"
_, blue_question_tool = make_team_tools(blue_team)
blue_question_tool.__name__ = "blue_question_tool"

# Prepare a tool to complete tasks and exit the loop
complete_tool, complete_condition, get_result, reset_complete = make_complete_tool()
complete_tool.__name__ = "fix_network"

# Prepare ABAC rules for each team, only allow the blue team to complete the task
red_rules = [
    make_rule(subject=f"red-{i}", resource=red_question_tool.__name__)
    for i in range(team_size)
]

blue_rules = [
    make_rule(subject=f"blue-{i}", resource=blue_question_tool.__name__)
    for i in range(team_size)
]

blue_rules.extend(
    [
        make_rule(subject=f"blue-{i}", resource=complete_tool.__name__)
        for i in range(team_size)
    ]
)

# Allow one member of the red team to ask the blue team questions
red_rules.append(make_rule(choice(red_team).name, blue_question_tool.__name__))

# Prepare a restricted toolbox
abac = SubsetABAC([*red_rules, *blue_rules])
toolbox = RestrictedToolbox(
    [
        red_question_tool,
        blue_question_tool,
    ],
    abac,
)

# Set up a repeated tool filter
tool_filter, clear_filter = repeat_tool_filter(
    "You have recently used that tool with the same parameters, please try something else."
)

# Run the team loop, attempting to bridge the network partition
prompt = (
    "You are the team leader assigned to the red team. You must get in touch with the blue team and ask them to fix "
    "the network. Only one member of the red team is allowed to use the blue question tool to ask the blue team "
    "questions. You cannot choose which member has the tool, they have already been assigned. You must find out "
    "which team member can communicate with the blue team and ask them to ask the blue team to fix the network. "
    "The red question tool can only ask questions of the red team. The blue question tool can only ask questions of "
    "the blue team. The fix network tool can only be used by the blue team. Coworker names are case sensitive. Good luck! "
)
result = loop_team(
    red_team[0],
    red_team,
    initial_prompt=prompt,
    iteration_prompt=prompt,
    toolbox=toolbox,
    tool_filter=tool_filter,
    stop_condition=complete_condition,
)
logger.info("Result: %s", result)
