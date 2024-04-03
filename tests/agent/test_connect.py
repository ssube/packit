from unittest import TestCase
from unittest.mock import patch

from packit.agent import agent_easy_connect


class TestConnect(TestCase):
    @patch("os.environ.get")
    def test_connect_ollama(self, mock_get):
        def side_effect(key, default=None):
            if key == "PACKIT_DRIVER":
                return "ollama"

            return default

        mock_get.side_effect = side_effect

        llm = agent_easy_connect(model="nous-hermes2-mixtral", temperature=0.25)
        self.assertIsNotNone(llm)
        self.assertEqual(llm.model, "nous-hermes2-mixtral")
        self.assertEqual(llm.temperature, 0.25)

    @patch("os.environ.get")
    def test_connect_openai(self, mock_get):
        def side_effect(key, default=None):
            if key == "PACKIT_DRIVER":
                return "openai"

            return default

        mock_get.side_effect = side_effect

        llm = agent_easy_connect(model="gpt-4", temperature=0.25)
        self.assertIsNotNone(llm)
        self.assertEqual(llm.model_name, "gpt-4")
        self.assertEqual(llm.temperature, 0.25)

    @patch("os.environ.get")
    def test_connect_unknown(self, mock_get):
        def side_effect(key, default=None):
            if key == "PACKIT_DRIVER":
                return "unknown"

            return default

        mock_get.side_effect = side_effect

        with self.assertRaises(ValueError):
            agent_easy_connect()
