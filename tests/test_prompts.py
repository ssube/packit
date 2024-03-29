from unittest import TestCase

from packit.prompts import (
    PromptLibrary,
    get_function_example,
    get_prompts,
    get_random_prompt,
    set_default_library,
)


class TestPromptLibraryUtils(TestCase):
    def test_get_function_example(self):
        example = get_function_example()
        self.assertIsInstance(example, dict)

    def test_get_mixtral_prompts(self):
        prompts = get_prompts("mixtral")
        self.assertIsInstance(prompts, PromptLibrary)

    def test_get_smaug_prompts(self):
        prompts = get_prompts("smaug")
        self.assertIsInstance(prompts, PromptLibrary)

    def test_get_other_prompts(self):
        prompts = get_prompts("other")
        self.assertIsInstance(prompts, PromptLibrary)

    def test_get_random_prompt(self):
        prompt = get_random_prompt("function")
        self.assertIsInstance(prompt, str)

    def test_round_trip_library(self):
        library = PromptLibrary()
        set_default_library(library)
        self.assertEqual(get_prompts("other"), library)

    def test_missing_random_prompt(self):
        with self.assertRaises(KeyError):
            get_random_prompt("non_existent_prompt")
