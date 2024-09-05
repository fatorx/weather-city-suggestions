from app.core.config import settings
from app.vendors.weather import WeatherVendor
from app.vendors.gemini_llm import GeminiLLM


class VendorFactory:
    def create_weather(self) -> WeatherVendor:
        weather_url = settings.WEATHER_BASE_URL
        weather_api_key = settings.WEATHER_API_KEY

        weather = WeatherVendor(weather_url, weather_api_key)
        return weather

    def create_gemini_ll(self) -> WeatherVendor:
        gemini_model = settings.GEMINI_MODEL
        gemini_api_key = settings.GEMINI_API_KEY

        return GeminiLLM(gemini_model, gemini_api_key)
