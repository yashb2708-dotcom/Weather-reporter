# Weather Reporter

A Python project that fetches real-time weather data using REST APIs and provides formatted weather reports.

## Features
- Get weather for any city in the world
- REST API integration with Open-Meteo
- Unit tests with mocking
- GitHub Actions CI/CD pipeline

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python weather_reporter.py
```

Enter a city name (e.g., Dresden) and get a weather report.

## Testing

```bash
python -m pytest test_weather_reporter.py -v
```

## Files
- `weather_reporter.py` - Main application
- `test_weather_reporter.py` - Unit tests
- `requirements.txt` - Python dependencies
- `.github/workflows/ci.yml` - CI/CD pipeline