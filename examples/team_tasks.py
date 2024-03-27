from packit.agent import Agent, agent_easy_connect
from packit.conditions import condition_or, condition_threshold
from packit.filters import repeat_tool_filter
from packit.loops.legacy import loop_team
from packit.tools import Toolbox, make_complete_tool, make_team_tools
from packit.utils import logger_with_colors

logger = logger_with_colors(__name__)

# Set up some experts in different fields
llm = agent_easy_connect(model="mixtral", temperature=0.25)
coworkers = [
    Agent("mathematician", "You are a professional mathematician.", {}, llm),
    Agent("programmer", "You are an expert computer programmer.", {}, llm),
    Agent("writer", "You are an experienced novelist and creative writer.", {}, llm),
    Agent("biologist", "You are a doctor of biology.", {}, llm),
    Agent("historian", "You are a museum historian.", {}, llm),
]

coworker_names = [coworker.name for coworker in coworkers]


# Prepare a tool to complete tasks and exit the loop
complete_tool, complete_condition, reset_complete = make_complete_tool()
complete_or_threshold = condition_or(complete_condition, condition_threshold)


# Prepare the teamwork tools
delegate_tool, question_tool = make_team_tools(coworkers)


toolbox = Toolbox(
    [
        complete_tool,
        delegate_tool,
        question_tool,
    ]
)


# Prepare a filter to prevent repeated tool calls
tool_filter, clear_filter = repeat_tool_filter(
    "You have already used that tool, please try something else."
)


# Create a team leader
manager = Agent(
    "team leader",
    "You are the team leader. Complete your tasks by asking questions and delegating tasks to your coworkers.",
    {},
    llm,
)

# Complete some tasks
tasks = [
    "Write a novel about a haunted house.",
    "Calculate the square root of 144.",
    "Write a program that multiplies two numbers.",
    "Identify the genus of a tree with wide, five-pointed leaves.",
    "Research the history of the Roman Empire.",
]

for task in tasks:
    logger.info("Task: %s", task)
    clear_filter()
    reset_complete()

    loop_team(
        manager,
        coworkers,
        toolbox.definitions,
        toolbox.callbacks,
        (
            "Using your team, complete the following task: {task}. "
            "If you need help from an expert or more information, ask a question or delegate a task to your coworkers. "
            "Do not call the complete tool until the task is finished. "
            "Do not call the complete tool until you have received a response from your team. "
            "Do not describe what you are trying to accomplish. Only reply with function calls for tools. "
        ),
        (
            "You are trying to complete the following task with your team: {task}. "
            "If you have all of the information that you need, call the complete tool to finish the task. "
            "If the task is not complete, ask another question or delegate another task. "
            "Do not describe what you are trying to accomplish. Only reply with function calls for tools. "
        ),
        {
            "task": task,
        },
        stop_condition=complete_or_threshold,
        tool_filter=tool_filter,
    )

    if complete_condition():
        logger.info("Task complete.")
    else:
        logger.error("Task incomplete.")
