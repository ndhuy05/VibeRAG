"""
Test script for the /detect-ingredients API endpoint

This script demonstrates how to use the image ingredient detection endpoint.
You need a food image to test with.
"""

import requests
import base64
import sys
from pathlib import Path

API_URL = "http://localhost:8000/detect-ingredients"

def detect_ingredients_from_image(image_path: str, max_meals: int = 3):
    """
    Send image to API and get ingredient detection + meal recommendations
    
    Args:
        image_path: Path to the image file
        max_meals: Number of meals to return
    """
    # Check if file exists
    if not Path(image_path).exists():
        print(f"Error: File '{image_path}' not found!")
        return
    
    # Read and encode image to base64
    print(f"Reading image: {image_path}")
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode()
    
    # Prepare request
    payload = {
        "image": image_data,
        "max_meals": max_meals
    }
    
    # Send request
    print(f"\nSending request to {API_URL}...")
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        
        # Display results
        print("\n" + "="*60)
        print("🔍 DETECTED INGREDIENTS:")
        print("="*60)
        for i, ing in enumerate(result["detected_ingredients"], 1):
            print(f"  {i}. {ing}")
        
        print("\n" + "="*60)
        print("🤖 AI RESPONSE:")
        print("="*60)
        print(result["response"])
        
        print("\n" + "="*60)
        print(f"🍽️  MATCHING MEALS ({len(result['meals_used'])}):")
        print("="*60)
        for i, (meal, score) in enumerate(zip(result["meals_used"], result["scores"]), 1):
            print(f"\n{i}. {meal['name']} ({meal['category']})")
            print(f"   Origin: {meal['origin']}")
            print(f"   Relevance Score: {score:.1%}")
            print(f"   Ingredients: {', '.join([ing['name'] for ing in meal['ingredients'][:5]])}...")
            if meal.get('youtube_url'):
                print(f"   Video: {meal['youtube_url']}")
        
        print("\n" + "="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server.")
        print("Make sure the server is running: python main.py")
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ API Error: {e}")
        if response.text:
            print(f"Details: {response.text}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_image_detection.py <image_path> [max_meals]")
        print("\nExample:")
        print("  python test_image_detection.py food.jpg")
        print("  python test_image_detection.py salad.png 5")
        sys.exit(1)
    
    image_path = sys.argv[1]
    max_meals = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    detect_ingredients_from_image(image_path, max_meals)
