"""
Test script for weather-based meal suggestions
Usage: python test_weather_suggestions.py

NOTE: This is a TEST/DISPLAY script only.
- test_weather_suggestions(): Makes API call and RETURNS data (not prints)
- display_weather_results(): Displays the returned data (prints only)
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def display_weather_results(data: dict, location_name: str, lat: float, lon: float):
    """
    Display weather suggestion results to console
    
    IMPORTANT: This function only PRINTS data for viewing.
    It does NOT return anything. It's for human display only.
    
    Args:
        data: API response data dictionary
        location_name: Name of location tested
        lat: Latitude coordinate
        lon: Longitude coordinate
    """
    print(f"\n{'='*80}")
    print(f"🌤️  Weather Suggestions for {location_name}")
    print(f"📍 Coordinates: {lat}, {lon}")
    print(f"{'='*80}\n")
    
    # Display weather information
    print(f"🌍 Location: {data['location']}")
    print(f"🌡️  Temperature: {data['temperature']}°C")
    print(f"☁️  Weather: {data['weather_description']}")
    print(f"🎯 Condition: {data['weather_condition']}")
    print(f"\n{'─'*80}")
    
    # Display suggestions
    suggestions = data['suggestions']
    print(f"\n💡 Reasoning: {suggestions['reasoning']}")
    print(f"\n📋 Recommended Categories:")
    for cat in suggestions['recommended_categories']:
        print(f"   • {cat}")
    
    print(f"\n🔑 Search Keywords:")
    keywords = ", ".join(suggestions['recommended_keywords'][:8])
    print(f"   {keywords}")
    
    print(f"\n{'─'*80}")
    
    # Display recommended meals
    if data['recommended_meals']:
        print(f"\n🍳 Recommended Meals ({len(data['recommended_meals'])}):\n")
        for i, (meal, score) in enumerate(zip(data['recommended_meals'], data['scores']), 1):
            print(f"{i}. {meal['name']}")
            print(f"   Category: {meal['category']} | Origin: {meal['origin']}")
            print(f"   Match Score: {score:.1%}")
            print(f"   Ingredients: {', '.join([ing['name'] for ing in meal['ingredients'][:5]])}...")
            if meal.get('youtube_url'):
                print(f"   Video: {meal['youtube_url']}")
            print()
    else:
        print("\n⚠️  No specific meals found, but recommendations provided above.")
    
    print(f"{'─'*80}")
    
    # Display AI response
    print(f"\n🤖 AI Response:\n")
    print(data['ai_response'])
    
    print(f"\n{'─'*80}")
    
    # Display file info
    print(f"\n💾 Weather data saved to:")
    print(f"   📄 JSON File: {data['json_file']}")
    print(f"   📝 Text File: {data['text_file']}")
    
    print(f"\n{'='*80}\n")


def test_weather_suggestions(lat: float, lon: float, location_name: str, max_meals: int = 5):
    """
    Test the weather-based meal suggestions endpoint
    
    IMPORTANT: This function RETURNS the API response data.
    It does NOT print anything (display is handled separately).
    
    Args:
        lat: Latitude coordinate
        lon: Longitude coordinate
        location_name: Name of location
        max_meals: Number of meals to return
        
    Returns:
        dict: API response data if successful, None if failed
    """
    try:
        # Make API request
        response = requests.post(
            f"{BASE_URL}/weather-suggestions",
            json={
                "latitude": lat,
                "longitude": lon,
                "location_name": location_name,
                "max_meals": max_meals
            },
            timeout=30
        )
        
        if response.status_code == 200:
            # SUCCESS: Return the data (not print)
            data = response.json()
            
            # Display the results (for human viewing only)
            display_weather_results(data, location_name, lat, lon)
            
            # RETURN the actual data (this is what the caller gets)
            return data
        
        elif response.status_code == 503:
            # ERROR: Service unavailable
            print(f"\n{'='*80}")
            print(f"❌ Service Unavailable: {response.json()['detail']}")
            print("\n💡 Tips:")
            print("   1. Make sure you have set OPENWEATHER_API_KEY in config.py")
            print("   2. Get a free API key from: https://openweathermap.org/api")
            print("   3. Update backend/config.py with your API key")
            print(f"{'='*80}\n")
            return None
        
        else:
            # ERROR: Other error
            print(f"\n{'='*80}")
            print(f"❌ Error {response.status_code}: {response.text}")
            print(f"{'='*80}\n")
            return None
            
    except requests.exceptions.ConnectionError:
        # ERROR: Cannot connect
        print(f"\n{'='*80}")
        print("❌ Cannot connect to API. Make sure the server is running:")
        print("   cd backend")
        print("   python main.py")
        print(f"{'='*80}\n")
        return None
        
    except requests.exceptions.Timeout:
        # ERROR: Timeout
        print(f"\n{'='*80}")
        print("❌ Request timed out. Weather API might be slow.")
        print(f"{'='*80}\n")
        return None
        
    except Exception as e:
        # ERROR: Unknown error
        print(f"\n{'='*80}")
        print(f"❌ Error: {e}")
        print(f"{'='*80}\n")
        return None


def main():
    """
    Run tests for different locations and weather conditions
    
    This is the interactive CLI interface for testing.
    Uses test_weather_suggestions() to get data and displays results.
    """
    
    print("\n" + "="*80)
    print("🌤️  WEATHER-BASED MEAL SUGGESTIONS - TEST SUITE")
    print("="*80)
    
    # Test cases with different weather conditions
    test_locations = [
        {
            "name": "New York, USA",
            "lat": 40.7128,
            "lon": -74.0060,
            "description": "Testing cold weather (winter)"
        },
        {
            "name": "Miami, USA",
            "lat": 25.7617,
            "lon": -80.1918,
            "description": "Testing hot weather (tropical)"
        },
        {
            "name": "London, UK",
            "lat": 51.5074,
            "lon": -0.1278,
            "description": "Testing rainy/cloudy weather"
        },
        {
            "name": "Tokyo, Japan",
            "lat": 35.6762,
            "lon": 139.6503,
            "description": "Testing mild weather"
        },
        {
            "name": "Sydney, Australia",
            "lat": -33.8688,
            "lon": 151.2093,
            "description": "Testing southern hemisphere weather"
        }
    ]
    
    print("\nAvailable test locations:")
    for i, loc in enumerate(test_locations, 1):
        print(f"{i}. {loc['name']} - {loc['description']}")
    
    print("\n0. Test all locations")
    print("q. Quit")
    
    while True:
        choice = input("\nSelect location to test (0-5, q to quit): ").strip().lower()
        
        if choice == 'q':
            print("👋 Goodbye!")
            break
        
        elif choice == '0':
            print("\n🔄 Testing all locations...\n")
            for loc in test_locations:
                # Call test function - it returns data
                result = test_weather_suggestions(
                    lat=loc['lat'],
                    lon=loc['lon'],
                    location_name=loc['name'],
                    max_meals=3
                )
                
                # You can use the returned data here if needed
                if result:
                    print(f"✅ Successfully got data for {loc['name']}")
                    # Example: Access the data
                    # print(f"Temperature was: {result['temperature']}°C")
                
                input("Press Enter to continue to next location...")
            break
        
        elif choice.isdigit() and 1 <= int(choice) <= len(test_locations):
            loc = test_locations[int(choice) - 1]
            
            # Call test function - it returns the actual API response data
            result_data = test_weather_suggestions(
                lat=loc['lat'],
                lon=loc['lon'],
                location_name=loc['name'],
                max_meals=5
            )
            
            # The returned data can be used programmatically
            if result_data:
                print(f"\n📊 Data returned successfully!")
                print(f"   Type: {type(result_data)}")
                print(f"   Keys: {list(result_data.keys())[:5]}...")
                # You can now use result_data in your code
                # Example: save to file, send to another API, process further, etc.
        
        else:
            print("❌ Invalid choice. Please select 0-5 or q.")


if __name__ == "__main__":
    main()
