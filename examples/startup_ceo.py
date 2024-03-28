from packit.agent import Agent, agent_easy_connect
from packit.conditions import condition_or, condition_threshold
from packit.filters import repeat_tool_filter
from packit.loops import loop_team
from packit.memory import make_limited_memory
from packit.prompts import get_function_example, get_random_prompt
from packit.results import multi_function_result
from packit.tools import Toolbox, make_complete_tool, make_team_tools
from packit.utils import logger_with_colors

logger = logger_with_colors(__name__)

# Set up the available LLMs
llms = {
    "creative": agent_easy_connect(model="mixtral", temperature=0.75),
    "manager": agent_easy_connect(model="mixtral", temperature=0.05),
    "programmer": agent_easy_connect(
        model="knoopx/hermes-2-pro-mistral:7b-q8_0", temperature=0.15
    ),
}

# Set up shared memory
memory = make_limited_memory(100)


def get_shared_memory():
    return memory


# Set up the CEO
ceo = Agent(
    "CEO",
    "You are the CEO of a cutting-edge startup company developing amazing products.",
    {},
    llms["manager"],
    memory=get_shared_memory,
)

# Prepare a tool to recruit new coworkers
coworkers = [ceo]


def recruit_coworker(role: str, team: str, background: str) -> Agent:
    """
    Recruit a new coworker with the given role and background, and assign them to the given team.

    Args:
        role: The role of the new coworker.
        team: The team to assign the coworker to.
        background: The background of the new coworker.
    """
    team = team.lower()
    if team not in llms:
        return f"Unknown team {team}."

    names = [coworker.name.lower() for coworker in coworkers]
    if role.lower() in names:
        return f"Role {role} has already been filled."

    llm = llms[team]
    coworkers.append(
        Agent(
            role,
            f"You are a {background} You are working at a cutting-edge startup company developing amazing products.",
            {},
            llm,
            # memory=get_shared_memory,
        )
    )
    return f"Recruited a new {role}."


# Prepare a tool to complete tasks and exit the loop
complete_tool, complete_condition, reset_complete = make_complete_tool()
complete_or_threshold = condition_or(complete_condition, condition_threshold)


# Prepare the teamwork tools
delegate_tool, question_tool = make_team_tools(coworkers)

team_tools_notice = (
    "You can delegate tasks to your coworkers or ask them questions to help complete the product. "
    "If you are having trouble, ask the CEO for help and clearly describe the problem. "
    "When communicating with your coworkers, provide all of the information they need to complete the task. "
    "Do not assume they have any additional context. Do not delegate tasks to yourself. "
)


def get_budget_prompt() -> str:
    return f"Your remaining budget is ${budget}. Delegating a task costs you $1000, asking a question costs $100. "


def get_coworker_prompt(excluding: list[str] = []) -> list[str]:
    names = [coworker.name for coworker in coworkers if coworker.name not in excluding]
    return f"Your coworkers are named: {', '.join(names)}."


budget = 100_000
recursion_limit = 3
recursion_level = 0


def delegate_with_notice(
    coworker: str, task: str, context: dict[str, str] | None = None
) -> str:
    """
    Delegate a task to a coworker.

    Args:
        coworker: The name of the coworker.
        task: The task for the coworker to complete.
    """
    global budget
    global recursion_level

    context = context or {}

    if recursion_level >= recursion_limit:
        return "Cannot delegate task due to recursion limit."

    if budget <= 0:
        return "Cannot delegate task due to budget limit."

    budget -= 1_000
    recursion_level += 1
    result = delegate_tool(
        coworker,
        task
        + team_tools_notice
        + get_budget_prompt()
        + get_coworker_prompt(excluding=[coworker])
        + get_random_prompt("function"),
        context={
            **context,
            "example": get_function_example(),
            "tools": toolbox.definitions,
        },
    )
    recursion_level -= 1
    return result


def question_with_notice(
    coworker: str, question: str, context: dict[str, str] | None = None
) -> str:
    """
    Ask a question of a coworker.

    Args:
        coworker: The name of the coworker.
        question: The question to ask the coworker.
    """
    global budget
    global recursion_level

    context = context or {}

    if recursion_level >= recursion_limit:
        return "Cannot ask question due to recursion limit."

    if budget <= 0:
        return "Cannot ask question due to budget limit."

    budget -= 100
    recursion_level += 1
    result = question_tool(
        coworker,
        question
        + team_tools_notice
        + get_budget_prompt()
        + get_coworker_prompt(excluding=[coworker])
        + get_random_prompt("function"),
        context={
            **context,
            "example": get_function_example(),
            "tools": toolbox.definitions,
        },
    )
    recursion_level -= 1
    return result


toolbox = Toolbox(
    [
        complete_tool,
        delegate_with_notice,
        question_with_notice,
    ]
)

recruiting_toolbox = Toolbox(
    [
        recruit_coworker,
    ]
)

# Create some products
products = [
    "a new mobile app",
    "a blender for smoothies",
    "an umbrella that tells you the weather",
    "a robot that cleans your house",
    "a website for sharing cat pictures",
]

tool_filter, reset_filter = repeat_tool_filter(
    "You have already used that tool, please try something else.", search_window=100
)

for product in products:
    coworkers[:] = [ceo]
    recruiting = ceo(
        "Using the recruit coworker tool, recruit up to 6 coworkers to help develop {product}. "
        "Each coworker should have a unique role with an inspiring background. "
        "Assign each coworker to one of the following teams: {teams}. "
        " " + get_random_prompt("function"),
        example=get_function_example(),
        product=product,
        teams=list(llms.keys()),
        tools=recruiting_toolbox.definitions,
    )
    logger.info("Recruiting result: %s", recruiting)

    multi_function_result(recruiting, recruiting_toolbox.callbacks)
    logger.info("Coworkers: %s", [coworker.name for coworker in coworkers])

    # Reset the budget for each project
    budget = 25_000
    reset_complete()

    # Delegate tasks to the coworkers to develop the product
    while budget > 0 and not complete_condition():
        loop_team(
            ceo,
            coworkers,
            context={
                "budget": budget,
                "product": product,
            },
            initial_prompt=(
                "Come up with a compelling idea for {product} and plan the development process. "
                "Break down the development process into tasks and assign them to your coworkers. "
                "Keep track of the tasks and their progress. "
                "If you need more information or assistance, ask a question to your coworkers. "
                "When you are satisfied with the development, use the complete tool to finish the product."
            ),
            iteration_prompt=(
                "You are trying to complete development of the product: {product}. "
                "You can delegate tasks to your coworkers to help with the development. Keep track of the tasks and their progress. "
                "If you need more information or assistance, ask a question to your coworkers. "
                "" + get_budget_prompt() + ""
                "When you are satisfied with the development, use the complete tool to finish the product. "
                "Make sure to finish the product before you exhaust your budget. "
                "Your progress so far is: {memory}. "
            ),
            stop_condition=complete_or_threshold,
            toolbox=toolbox,
            tool_filter=tool_filter,
        )

    logger.info("Product development complete: %s", product)
