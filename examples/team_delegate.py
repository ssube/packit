from packit.agent import Agent, agent_easy_connect
from packit.prompts import get_function_example, get_random_prompt
from packit.results import multi_function_result
from packit.tools import make_team_tools, prepare_tools
from packit.utils import could_be_json, logger_with_colors

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
complete = False


def complete_tool(answer: str) -> str:
    """
    Complete a task.

    Args:
        answer: The answer to the task.
    """
    global complete
    complete = True

    logger.info("Task answer: %s", answer)
    return "Task complete."


# Prepare the teamwork tools
delegate_tool, question_tool = make_team_tools(coworkers)


tools, tool_dict = prepare_tools(
    [
        complete_tool,
        delegate_tool,
        question_tool,
    ]
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
    result = manager(
        "Using your team, complete the following task: {task} "
        "Your team includes coworkers named: {names}. " + get_random_prompt("function"),
        names=coworker_names,
        task=task,
        example=get_function_example(),
        tools=tools,
    )
    logger.info("Result: %s", result)

    answers = []
    complete = False

    while not complete:
        if could_be_json(result):
            new_answers = multi_function_result(result, tool_dict)
        else:
            new_answers = [result]

        answers.extend(new_answers)

        # Provide the response to the team leader
        result = manager(
            "You are trying to complete the following task with your team: {task}. "
            "If you have all of the information that you need, call the complete tool to finish the task. "
            "If the task is not complete, ask another question or delegate another task. "
            "Your team includes coworkers named: {names}. "
            "Your coworkers have provided the following answers to your previous questions: {answers}. ",
            answers=answers,
            names=coworker_names,
            task=task,
        )
        logger.info("Response: %s", result)

    logger.info("Task complete.")
