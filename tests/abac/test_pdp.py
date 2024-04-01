from unittest import TestCase

from py_abac import PDP, Policy
from py_abac.storage.memory import MemoryStorage

from packit.abac.pdp import PDPABAC


class TestPDP(TestCase):
    def test_pdp(self):
        # Policy definition in JSON
        policy_json = {
            "uid": "1",
            "description": "Max and Nina are allowed to create, delete, get any "
            "resources only if the client IP matches.",
            "effect": "allow",
            "rules": {
                "subject": [
                    {"$.name": {"condition": "Equals", "value": "Max"}},
                    {"$.name": {"condition": "Equals", "value": "Nina"}},
                ],
                "resource": {"$.name": {"condition": "RegexMatch", "value": ".*"}},
                "action": [
                    {"$.method": {"condition": "Equals", "value": "create"}},
                    {"$.method": {"condition": "Equals", "value": "delete"}},
                    {"$.method": {"condition": "Equals", "value": "get"}},
                ],
                "context": {"$.ip": {"condition": "CIDR", "value": "127.0.0.1/32"}},
            },
            "targets": {},
            "priority": 0,
        }
        # Parse JSON and create policy object
        policy = Policy.from_json(policy_json)

        # Setup policy storage
        storage = MemoryStorage()
        storage.add(policy)

        # Create policy decision point
        pdp = PDP(storage)
        abac = PDPABAC(pdp)
        self.assertTrue(
            abac.check(
                {
                    "subject": "Max",
                    "resource": "test",
                    "action": "create",
                    "ip": "127.0.0.1",
                }
            )
        )
