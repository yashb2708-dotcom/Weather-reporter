import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_coordinates(city):
    """Get latitude and longitude for a city."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('results'):
            result = data['results'][0]
            return result['latitude'], result['longitude']
        else:
            logger.error(f"City '{city}' not found")
            return None, None
    except requests.RequestException as e:
        logger.error(f"Error fetching coordinates: {e}")
        return None, None

def get_weather(lat, lon):
    """Get weather data for coordinates."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=weather_code,temperature_2m,wind_speed_10m"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        current = data.get('current', {})
        return {
            'temperature': current.get('temperature_2m'),
            'weather_code': current.get('weather_code'),
            'wind_speed': current.get('wind_speed_10m')
        }
    except requests.RequestException as e:
        logger.error(f"Error fetching weather: {e}")
        return None

def describe_weather(code):
    """Convert weather code to description."""
    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy (rime)",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
    }
    return codes.get(code, "Unknown weather")

def build_report(city, weather):
    """Build a formatted weather report."""
    if not weather:
        return f"Could not fetch weather for {city}"
    
    temp = weather['temperature']
    description = describe_weather(weather['weather_code'])
    wind = weather['wind_speed']
    
    report = f"""
╔═══════════════════════════════════════╗
║     WEATHER REPORT FOR {city.upper():^31} ║
╚═══════════════════════════════════════╝
🌡️  Temperature: {temp}°C
🌤️  Condition: {description}
💨 Wind Speed: {wind} km/h
"""
    return report

if __name__ == "__main__":
    city = input("Enter a city name: ").strip()
    if city:
        lat, lon = get_coordinates(city)
        if lat and lon:
            weather = get_weather(lat, lon)
            report = build_report(city, weather)
            print(report)
    else:
        print("No city entered")