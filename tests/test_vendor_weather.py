import os
import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.vendors.weather import WeatherVendor, ResponseWeather

from dotenv import load_dotenv

load_dotenv()


@patch('app.core.cache.get_cache')
@patch('app.core.cache.set_cache')
@patch('requests.get')
class TestWeatherVendor(unittest.TestCase):

    def setUp(self):
        self.host = os.getenv('WEATHER_BASE_URL')
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.weather_vendor = WeatherVendor(self.host, self.api_key)

    def test_get_weather_by_city_cache_hit(self, mock_requests_get, mock_set_cache, mock_get_cache):
        mock_get_cache.return_value = b'{"weather": [{"description": "clear sky"}], "main": {"temp": 298.15}}'

        mock_requests_get.status_code = 200
        response = self.weather_vendor.get_weather_by_city("Curitiba")

        self.assertIsInstance(response, ResponseWeather)
        self.assertEqual(response.city, "Curitiba")
        self.assertEqual(response.description, "clear sky")
        self.assertEqual(response.temperature, "25.0°C")
        mock_requests_get.assert_not_called()
        mock_set_cache.assert_not_called()

    def test_get_weather_by_city_api_call_success(self, mock_requests_get, mock_set_cache, mock_get_cache):
        mock_get_cache.return_value = None
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "weather": [{"description": "light rain"}],
            "main": {"temp": 285.15}
        }
        mock_requests_get.return_value = mock_response

        response = self.weather_vendor.get_weather_by_city("London")

        self.assertIsInstance(response, ResponseWeather)
        self.assertEqual(response.city, "London")
        self.assertEqual(response.description, "Light rain")
        self.assertEqual(response.temperature, "12.0°C")
        mock_requests_get.assert_called_once_with(
            f"{self.host}?appid={self.api_key}&q=London"
        )

    def test_get_weather_by_city_api_call_failure(self, mock_requests_get, mock_set_cache, mock_get_cache):
        mock_get_cache.return_value = None
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        with self.assertRaises(HTTPException) as cm:
            self.weather_vendor.get_weather_by_city("InvalidCity")

        self.assertEqual(cm.exception.status_code, 400)
        self.assertEqual(cm.exception.detail, "Implement this message!")
        mock_set_cache.assert_not_called()

    def test_get_weather_format_valid_data(self, mock_requests_get, mock_set_cache, mock_get_cache):
        data = {
            "weather": [{"description": "scattered clouds"}],
            "main": {"temp": 290.15}
        }
        formatted_temperature, weather_description = self.weather_vendor.get_weather_format(data)

        self.assertEqual(formatted_temperature, "17.0°C")
        self.assertEqual(weather_description, "Scattered clouds")

    def test_get_weather_format_invalid_data(self, mock_requests_get, mock_set_cache, mock_get_cache):
        data = {"main": {"temp": 290.15}}

        with self.assertRaises(HTTPException) as cm:
            self.weather_vendor.get_weather_format(data)

        self.assertEqual(cm.exception.status_code, 400)
        self.assertEqual(cm.exception.detail, "Error: Invalid or incomplete weather data.")
