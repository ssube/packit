from py_abac import PDP, Request

from packit.types import ABACAdapter, ABACAttributes, RuleState

REQUIRED_ATTRIBUTES = ["subject", "resource", "action"]


class PDPABAC(ABACAdapter):
    pdp: PDP

    def __init__(
        self,
        pdp: PDP,
    ):
        self.pdp = pdp

    def select(
        self, attributes: ABACAttributes
    ) -> tuple[str, str, str, dict[str, str]]:
        """
        Select the subject, resource, and action from the attributes.
        """

        subject = attributes["subject"]
        resource = attributes["resource"]
        action = attributes["action"]

        return subject, resource, action, attributes

    def check(self, attributes: ABACAttributes) -> RuleState:
        """
        Check if the agent has access to the tool.
        """

        subject, resource, action, context = self.select(attributes)

        request_json = {
            "subject": {"id": "", "attributes": {"name": subject}},
            "resource": {"id": "", "attributes": {"name": resource}},
            "action": {"id": "", "attributes": {"method": action}},
            "context": context,
        }
        request = Request.from_json(request_json)

        return self.pdp.is_allowed(request)
