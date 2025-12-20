import requests
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from backend import config

def fetch_weather(lat: float, lon: float, api_key: str) -> Optional[Dict[str, Any]]:
    """
    Fetch weather data from OpenWeatherMap API
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        Dictionary containing weather data or None if request fails
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric"  # Use metric units for temperature
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        weather_data = response.json()

        return weather_data
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    
if __name__ == "__main__":
    # Example usage
    lat = 40.7128
    lon = -74.0060
    weather_data = fetch_weather(lat, lon, api_key=config.OPENWEATHER_API_KEY)
    if weather_data:
        print(json.dumps(weather_data, indent=2))
    else:
        print("Failed to fetch weather data.")