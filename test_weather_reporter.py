import unittest
from unittest.mock import patch, MagicMock
import weather_reporter

class TestWeatherReporter(unittest.TestCase):
    
    @patch('weather_reporter.requests.get')
    def test_get_coordinates(self, mock_get):
        """Test getting coordinates from city name."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [{
                'latitude': 51.05,
                'longitude': 13.74
            }]
        }
        mock_get.return_value = mock_response
        
        lat, lon = weather_reporter.get_coordinates('Dresden')
        self.assertEqual(lat, 51.05)
        self.assertEqual(lon, 13.74)
    
    @patch('weather_reporter.requests.get')
    def test_get_weather(self, mock_get):
        """Test getting weather for coordinates."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'current': {
                'temperature_2m': 15.5,
                'weather_code': 61,
                'wind_speed_10m': 12.3
            }
        }
        mock_get.return_value = mock_response
        
        weather = weather_reporter.get_weather(51.05, 13.74)
        self.assertEqual(weather['temperature'], 15.5)
        self.assertEqual(weather['weather_code'], 61)
        self.assertEqual(weather['wind_speed'], 12.3)
    
    def test_describe_weather(self):
        """Test weather code to description conversion."""
        self.assertEqual(weather_reporter.describe_weather(0), "Clear sky")
        self.assertEqual(weather_reporter.describe_weather(61), "Slight rain")
        self.assertEqual(weather_reporter.describe_weather(95), "Thunderstorm")
        self.assertEqual(weather_reporter.describe_weather(999), "Unknown weather")
    
    def test_build_report(self):
        """Test building the weather report."""
        weather = {
            'temperature': 15.5,
            'weather_code': 61,
            'wind_speed': 12.3
        }
        report = weather_reporter.build_report('Dresden', weather)
        self.assertIn('DRESDEN', report)
        self.assertIn('15.5°C', report)
        self.assertIn('Slight rain', report)
        self.assertIn('12.3 km/h', report)

if __name__ == '__main__':
    unittest.main()