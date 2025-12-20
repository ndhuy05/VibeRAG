"""
Weather Service for fetching weather data and storing it as chunkable text files.
Uses OpenWeatherMap API to get current weather based on coordinates.
"""

import requests
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import config
from models import Meal


class WeatherService:
    """Service for fetching and managing weather data"""
    
    def __init__(self, gemini_service=None):
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = config.OPENWEATHER_API_KEY
        self.weather_data_dir = config.WEATHER_DATA_DIR
        self.weather_data_dir.mkdir(exist_ok=True)
        self.gemini_service = gemini_service
        
    def fetch_weather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Fetch weather data from OpenWeatherMap API
        Args:
            lat: Latitude
            lon: Longitude
        Returns:
            Dictionary containing weather data or None if request fails
        """
        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"  # Use metric units for temperature
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            weather_data = response.json()
            return weather_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def save_weather_to_file(self, weather_data: Dict[str, Any], location_name: str = None) -> Dict[str, str]:
        """
        Save weather data to separate JSON and text files in a chunkable format
        
        Args:
            weather_data: Weather data from API
            location_name: Optional custom location name
            
        Returns:
            Dictionary with paths to both saved files (json_file, text_file)
        """
        if not weather_data:
            raise ValueError("No weather data to save")
        
        # Generate base filename based on location and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        location = location_name or weather_data.get("name", "unknown")
        base_filename = f"{location}_{timestamp}"
        
        # File paths
        json_filepath = self.weather_data_dir / f"{base_filename}.json"
        text_filepath = self.weather_data_dir / f"{base_filename}.txt"
        
        # Extract relevant weather information
        main = weather_data.get("main", {})
        weather = weather_data.get("weather", [{}])[0]
        wind = weather_data.get("wind", {})
        clouds = weather_data.get("clouds", {})
        sys_data = weather_data.get("sys", {})
        
        # 1. Save JSON data file
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, indent=2, ensure_ascii=False)
        
        # 2. Create and save human-readable text format
        weather_text = f"""Weather Report for {weather_data.get('name', 'Unknown Location')}
            Location: {weather_data.get('name', 'Unknown')}, {sys_data.get('country', 'N/A')}
            Coordinates: Latitude {weather_data.get('coord', {}).get('lat', 'N/A')}, Longitude {weather_data.get('coord', {}).get('lon', 'N/A')}
            Date and Time: {datetime.fromtimestamp(weather_data.get('dt', 0)).strftime('%Y-%m-%d %H:%M:%S')}
            Timezone: UTC{weather_data.get('timezone', 0) // 3600:+d}

            Current Conditions:
            ------------------
            Weather: {weather.get('main', 'N/A')} - {weather.get('description', 'N/A')}
            Temperature: {main.get('temp', 'N/A')}°C
            Feels Like: {main.get('feels_like', 'N/A')}°C
            Temperature Range: {main.get('temp_min', 'N/A')}°C to {main.get('temp_max', 'N/A')}°C
            Humidity: {main.get('humidity', 'N/A')}%
            Pressure: {main.get('pressure', 'N/A')} hPa
            Visibility: {weather_data.get('visibility', 'N/A')} meters

            Wind Conditions:
            ---------------
            Wind Speed: {wind.get('speed', 'N/A')} m/s
            Wind Direction: {wind.get('deg', 'N/A')}°
            Wind Gust: {wind.get('gust', 'Not reported')} m/s

            Cloud Coverage:
            --------------
            Cloudiness: {clouds.get('all', 'N/A')}%

            Additional Information:
            ----------------------
            Sunrise: {datetime.fromtimestamp(sys_data.get('sunrise', 0)).strftime('%H:%M:%S') if sys_data.get('sunrise') else 'N/A'}
            Sunset: {datetime.fromtimestamp(sys_data.get('sunset', 0)).strftime('%H:%M:%S') if sys_data.get('sunset') else 'N/A'}
            """
        
        with open(text_filepath, 'w', encoding='utf-8') as f:
            f.write(weather_text)
        
        return {
            "json_file": str(json_filepath),
            "text_file": str(text_filepath)
        }
    
    def get_weather_and_save(self, lat: float, lon: float, location_name: str = None) -> Optional[Dict[str, Any]]:
        """
        Fetch weather data and save it to separate JSON and text files
        
        Args:
            lat: Latitude
            lon: Longitude
            location_name: Optional custom location name
            
        Returns:
            Dictionary with weather data and file paths
        """
        weather_data = self.fetch_weather(lat, lon)
        
        if weather_data:
            file_paths = self.save_weather_to_file(weather_data, location_name)
            return {
                "weather_data": weather_data,
                "json_file": file_paths["json_file"],
                "text_file": file_paths["text_file"],
                "timestamp": datetime.now().isoformat()
            }
        
        return None
    
    def get_weather_condition(self, weather_data: Dict[str, Any]) -> str:
        """
        Get simplified weather condition from weather data
        
        Returns: 'hot', 'cold', 'rainy', 'cloudy', 'clear', etc.
        """
        if not weather_data:
            return "unknown"
        
        temp = weather_data.get("main", {}).get("temp", 20)
        weather_main = weather_data.get("weather", [{}])[0].get("main", "").lower()
        
        # Categorize based on temperature and conditions
        if temp > 30:
            return "hot"
        elif temp < 10:
            return "cold"
        elif "rain" in weather_main or "drizzle" in weather_main:
            return "rainy"
        elif "snow" in weather_main:
            return "snowy"
        elif "cloud" in weather_main:
            return "cloudy"
        elif "clear" in weather_main:
            return "clear"
        else:
            return "mild"
    
    def suggest_meal_categories_for_weather(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest meal types based on current weather
        
        Returns:
            Dictionary with suggestions and reasoning
        """
        condition = self.get_weather_condition(weather_data)
        temp = weather_data.get("main", {}).get("temp", 20)
        weather_desc = weather_data.get("weather", [{}])[0].get("description", "")
        
        suggestions = {
            "condition": condition,
            "temperature": temp,
            "description": weather_desc,
            "recommended_categories": [],
            "recommended_keywords": [],
            "reasoning": ""
        }
        
        if condition == "hot":
            suggestions["recommended_categories"] = ["Salad", "Seafood", "Vegan", "Starter"]
            suggestions["recommended_keywords"] = ["salad", "cold", "refreshing", "light", "grilled", "fresh", "chilled"]
            suggestions["reasoning"] = f"It's hot outside ({temp}°C). Light, refreshing meals like salads and cold dishes are perfect."
            
        elif condition == "cold":
            suggestions["recommended_categories"] = ["Soup", "Beef", "Pork", "Chicken", "Lamb"]
            suggestions["recommended_keywords"] = ["soup", "stew", "hot", "warm", "hearty", "roast", "braised", "comfort"]
            suggestions["reasoning"] = f"It's cold outside ({temp}°C). Warm, hearty meals like soups and stews will keep you cozy."
            
        elif condition == "rainy":
            suggestions["recommended_categories"] = ["Soup", "Chicken", "Pasta", "Beef"]
            suggestions["recommended_keywords"] = ["soup", "stew", "comfort", "warm", "cozy", "pasta", "noodles", "hot"]
            suggestions["reasoning"] = f"It's rainy outside. Comfort food like soups, pasta, and warm dishes are ideal."
            
        elif condition == "snowy":
            suggestions["recommended_categories"] = ["Soup", "Beef", "Pork", "Dessert"]
            suggestions["recommended_keywords"] = ["soup", "stew", "roast", "hot", "warm", "hearty", "thick", "rich"]
            suggestions["reasoning"] = f"It's snowy outside ({temp}°C). Rich, hearty meals will warm you up."
            
        else:  # mild, clear, cloudy
            suggestions["recommended_categories"] = ["Chicken", "Pasta", "Seafood", "Vegetarian"]
            suggestions["recommended_keywords"] = ["grilled", "baked", "roasted", "fresh", "balanced"]
            suggestions["reasoning"] = f"Nice weather ({temp}°C, {weather_desc}). Any balanced meal would be great!"
        
        return suggestions
    
    def generate_weather_meal_response(
        self, 
        weather_data: Dict[str, Any],
        meals: List[Meal],
        scores: List[float],
        location: str
    ) -> str:
        """
        Generate AI response for weather-based meal suggestions using Gemini
        
        Args:
            weather_data: Weather data from API
            meals: List of recommended meals
            scores: Similarity scores for meals
            location: Location name
            
        Returns:
            AI-generated response
        """
        if not self.gemini_service:
            # Fallback response without Gemini
            suggestions = self.suggest_meal_categories_for_weather(weather_data)
            return suggestions["reasoning"]
        
        # Get weather suggestions
        suggestions = self.suggest_meal_categories_for_weather(weather_data)
        temp = weather_data.get("main", {}).get("temp", 0)
        weather_desc = weather_data.get("weather", [{}])[0].get("description", "")
        
        # Create meal context similar to gemini_service format
        meal_context = ""
        if meals:
            meal_context = "\n\nHere are the recommended meals I found:\n\n"
            for i, (meal, score) in enumerate(zip(meals, scores), 1):
                meal_context += f"### {i}. {meal.name}\n"
                meal_context += f"- **Category**: {meal.category}\n"
                meal_context += f"- **Origin**: {meal.origin}\n"
                meal_context += f"- **Match Score**: {score:.1%}\n"
                
                # Add ingredients
                meal_context += f"- **Ingredients**: "
                ingredient_names = [ing.name for ing in meal.ingredients[:8]]
                meal_context += ", ".join(ingredient_names)
                if len(meal.ingredients) > 8:
                    meal_context += f", and {len(meal.ingredients) - 8} more"
                meal_context += "\n"
                
                # Add recipe snippet
                if meal.recipe:
                    recipe_snippet = meal.recipe[:150].replace('\n', ' ').strip()
                    if len(meal.recipe) > 150:
                        recipe_snippet += "..."
                    meal_context += f"- **Recipe**: {recipe_snippet}\n"
                
                if meal.youtube_url:
                    meal_context += f"- **Video Tutorial**: {meal.youtube_url}\n"
                
                meal_context += "\n"
        
        # Create prompt for Gemini
        prompt = f"""You are a helpful cooking assistant with expertise in weather-based meal recommendations.

Current Weather in {location}:
- Temperature: {temp}°C
- Condition: {weather_desc}
- Weather Type: {suggestions['condition']}

Weather Analysis:
{suggestions['reasoning']}

Recommended Categories: {', '.join(suggestions['recommended_categories'])}
Best Meal Types: {', '.join(suggestions['recommended_keywords'][:6])}
{meal_context}

Based on the current weather conditions and the meals above, please provide a warm, conversational response that:
- Acknowledges the weather conditions in {location}
- Explains why these meal types are perfect for this weather
- Highlights 2-3 specific recommended meals from the list (if available)
- Mentions key ingredients or cooking methods that work well in this weather
- Provides helpful cooking tips related to the weather (e.g., "perfect day for slow cooking" or "keep it light and fresh")
- Be friendly, enthusiastic, and concise (2-3 paragraphs)
- Include YouTube links if asking about videos

Response:"""
        
        try:
            # Generate response using Gemini
            response = self.gemini_service.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            # Fallback to simple reasoning if Gemini fails
            print(f"Error generating Gemini response: {e}")
            fallback = f"{suggestions['reasoning']}\n\n"
            if meals:
                fallback += f"I've found {len(meals)} meals that would be perfect for this weather: "
                fallback += ", ".join([meal.name for meal in meals[:3]])
                if len(meals) > 3:
                    fallback += f", and {len(meals) - 3} more."
            else:
                fallback += f"I recommend exploring {', '.join(suggestions['recommended_categories'][:3])} dishes."
            return fallback


# Singleton instance
_weather_service = None

def get_weather_service(gemini_service=None) -> WeatherService:
    """Get or create weather service instance"""
    global _weather_service
    if _weather_service is None:
        _weather_service = WeatherService(gemini_service)
    elif gemini_service and not _weather_service.gemini_service:
        _weather_service.gemini_service = gemini_service
    return _weather_service
