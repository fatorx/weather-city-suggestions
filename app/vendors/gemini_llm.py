import re
import google.generativeai as genai
from google.generativeai import GenerationConfig
from google.generativeai.types import HarmCategory, HarmBlockThreshold


class GeminiLLM:

    def __init__(self, model: str, api_key: str):
        genai.configure(api_key=api_key)

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 50,
            "response_mime_type": "text/plain",
        }
        gen_config = GenerationConfig(**self.generation_config)

        self.model = genai.GenerativeModel(
            model_name=model,
            generation_config=gen_config,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }
        )

        self.chat_session = self.model.start_chat(
            history=self.get_chat_history()
        )

    def get_chat_history(self):
        history = [
            {
                "role": "user",
                "parts": [
                    "São Paulo, 24.3, clear sky",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Em São Paulo, o sol tá brilhando e o céu tá azul, aproveite o dia lindo! ☀️\n",
                ],
            },
            {
                "role": "user",
                "parts": [
                    "Ushuaia,2.8,broken clouds",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Ushuaia, tá frio, mas o sol ainda te espera entre as nuvens! 🥶☀️ \n",
                ],
            },
            {
                "role": "user",
                "parts": [
                    "São Paulo, 24.3, clear sky",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "São Paulo, sol de rachar, aproveita que hoje tá um dia lindo! ☀️ \n",
                ],
            },
            {
                "role": "user",
                "parts": [
                    "São Paulo, 24.3, clear sky",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Em São Paulo, sol de rachar, aproveita que hoje tá um dia lindo! ☀️ \n",
                ],
            },
        ]
        return history

    def send_message(self, text) -> str:
        response = self.chat_session.send_message(text)
        text = response.text
        clear_text = re.sub(r'[\n\r]', '', text)

        return clear_text.strip()
