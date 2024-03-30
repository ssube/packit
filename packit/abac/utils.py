from .adapter import RuleState, StateRule


def make_rule(
    subject: str | None = None,
    resource: str | None = None,
    action: str | None = None,
    context: str | None = None,
    state: RuleState = RuleState.ALLOW,
) -> StateRule:
    """
    Create a rule for an agent to perform an action on a resource.
    """

    criteria = {}

    # TODO: automatically get name from agents here
    if subject:
        criteria["subject"] = subject

    if resource:
        criteria["resource"] = resource

    if action:
        criteria["action"] = action

    if context:
        criteria.update(context)

    return (criteria, state)
