from app.vendors.gemini_llm import GeminiLLM
from app.vendors.weather import WeatherVendor


class SentenceCreatorService:

    def __init__(self, weather: WeatherVendor, gemini_llm: GeminiLLM):
        self.weather = weather
        self.gemini_llm = gemini_llm

    async def process_input(self, city: str) -> str:
        response_weather = self.weather.get_weather_by_city(city)
        message = response_weather.get_message()

        return self.gemini_llm.send_message(message)
