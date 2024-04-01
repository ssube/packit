from .subset import GenericRule, RuleState


def make_rule(
    subject: str | None = None,
    resource: str | None = None,
    action: str | None = None,
    context: str | None = None,
    state: RuleState = RuleState.ALLOW,
) -> GenericRule:
    """
    Create a rule for an agent to perform an action on a resource.
    """

    criteria = {}

    if context:
        criteria.update(context)

    if action:
        criteria["action"] = action

    if resource:
        criteria["resource"] = resource

    # TODO: automatically get name from agents here
    if subject:
        criteria["subject"] = subject

    return (criteria, state)
