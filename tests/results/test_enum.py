from unittest import TestCase

from packit.results import enum_result


class TestEnumResult(TestCase):
    def test_valid_value(self):
        self.assertEqual(enum_result("yes", enum=["yes", "no"]), "yes")

    def test_invalid_value(self):
        self.assertEqual(enum_result("maybe", enum=["yes", "no"]), None)

    def test_first_value(self):
        self.assertEqual(enum_result("yes and no", enum=["yes", "no"]), "yes")


if __name__ == "__main__":
    from unittest import main

    main()
