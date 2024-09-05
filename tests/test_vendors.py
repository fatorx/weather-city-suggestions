import unittest
from unittest.mock import patch, MagicMock
import re

from app.vendors.gemini_llm import GeminiLLM
from app.prompts.instructions import Instructions

class TestGeminiLLM(unittest.TestCase):

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_init(self, mock_model, mock_configure):
        mock_model_instance = MagicMock()
        mock_model_instance.start_chat.return_value = MagicMock()
        mock_model.return_value = mock_model_instance

        model_name = "test_model"
        api_key = "test_api_key"
        llm = GeminiLLM(model_name, api_key)

        mock_configure.assert_called_once_with(api_key=api_key)
        mock_model.assert_called_once_with(
            model_name=model_name,
            generation_config=unittest.mock.ANY,
            system_instruction=Instructions.SENTENCE_CITY_WEATHER
        )

        mock_model_instance.start_chat.assert_called_once()

    @patch('google.generativeai.GenerativeModel')
    def test_send_message(self, mock_model):

        mock_chat_session = MagicMock()
        mock_chat_session.send_message.return_value = MagicMock(text="  Hello\nWorld!  \r\n")
        mock_model_instance = MagicMock()
        mock_model_instance.start_chat.return_value = mock_chat_session
        mock_model.return_value = mock_model_instance

        llm = GeminiLLM("test_model", "test_api_key")

        response = llm.send_message("Test message")
        self.assertEqual(response, "HelloWorld!")
