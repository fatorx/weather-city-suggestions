import requests
import json
from fastapi import HTTPException
from app.core.cache import get_cache, set_cache
from app.messages.messages import Messages

EXPIRE_CACHE = 60


class ResponseWeather:

    def __init__(self, city: str, description: str, temperature: float):
        self.city = city
        self.description = description
        self.temperature = temperature

    def get_message(self):
        return f'{self.city}, {self.description}, {self.temperature}'


class WeatherVendor:
    def __init__(self, host: str, api_key: str):
        self.host = host
        self.api_key = api_key

    def get_weather_by_city(self, city: str) -> ResponseWeather:
        cache_data = get_cache(city)
        if cache_data:
            weather_data = json.loads(cache_data.decode('utf-8'))
            formatted_temperature, weather_description = self.get_weather_format(weather_data)
            return ResponseWeather(city, weather_description, formatted_temperature)

        request_url = f'{self.host}?appid={self.api_key}&q={city}'
        response = requests.get(request_url)

        if response.status_code == 200:
            data = response.json()
            set_cache(city, json.dumps(data), EXPIRE_CACHE)
            formatted_temperature, weather_description = self.get_weather_format(data)

            return ResponseWeather(city, weather_description, formatted_temperature)
        else:
            raise HTTPException(status_code=400, detail=Messages.WEATHER_API_ERROR)

    def get_weather_format(self, data):
        """
        Extracts and formats weather information from the provided data.

        Args:
            data (dict): The weather data containing 'weather' and 'main' sections.

        Returns:
            tuple: A tuple containing the formatted temperature in Celsius and the weather description.
        """
        try:
            weather_description = data['weather'][0]['description'].capitalize()

            temperature_kelvin = data['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15
            formatted_temperature = f"{temperature_celsius:.1f}°C"

            return formatted_temperature, weather_description

        except (KeyError, IndexError):
            raise HTTPException(status_code=400, detail=Messages.WEATHER_API_ERROR)
