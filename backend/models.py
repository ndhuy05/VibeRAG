from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Ingredient(BaseModel):
    """Ingredient with name and quantity"""
    name: str = Field(..., description="Ingredient name", example="Chicken")
    quantity: str = Field(..., description="Quantity/measurement", example="500g")

class Meal(BaseModel):
    """Complete meal information with ingredients and recipe"""
    name: str = Field(..., description="Meal name", example="Chicken Curry")
    category: str = Field(..., description="Meal category", example="Chicken")
    origin: str = Field(..., description="Country of origin", example="Indian")
    ingredients: List[Ingredient] = Field(..., description="List of ingredients")
    recipe: str = Field(..., description="Cooking instructions", example="Heat oil in a pan...")
    youtube_url: Optional[str] = Field(None, description="YouTube tutorial URL", example="https://www.youtube.com/watch?v=xxxxx")
    
class SearchRequest(BaseModel):
    """Request model for ingredient search"""
    ingredients: List[str] = Field(..., description="List of ingredient names to search for")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results to return")
    category: Optional[str] = Field(default=None, description="Filter by category (e.g., Beef, Chicken)")
    
class MealResult(BaseModel):
    """Search result with similarity score"""
    meal: Meal
    score: float = Field(..., description="Similarity score (0-1, higher is better)")
    
class SearchResponse(BaseModel):
    """Response model for search results"""
    query_ingredients: List[str]
    results: List[MealResult]
    total_results: int
    
class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    total_meals: int
    index_initialized: bool

class ChatRequest(BaseModel):
    """Chat request with user query"""
    query: str = Field(
        ...,
        description="Your question about meals or recipes",
        example="Find me a chicken curry recipe"
    )
    max_meals: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of meals to return (1-10)"
    )
    category: Optional[str] = Field(
        default=None,
        description="Filter by category (e.g., Chicken, Beef, Vegetarian)",
        example="Chicken"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Find me a chicken curry recipe",
                "max_meals": 3,
                "category": "Chicken"
            }
        }

class ChatResponse(BaseModel):
    """Chat response with AI-generated answer and relevant meals"""
    query: str = Field(..., description="Original user query")
    response: str = Field(..., description="AI-generated response text")
    meals_used: List[Meal] = Field(..., description="List of relevant meals found")
    scores: List[float] = Field(..., description="Similarity scores for each meal (0-1, higher is better)")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Find me a chicken curry recipe",
                "response": "Here are some delicious chicken curry recipes...",
                "meals_used": [
                    {
                        "name": "Chicken Curry",
                        "category": "Chicken",
                        "origin": "Indian",
                        "ingredients": [
                            {"name": "Chicken", "quantity": "500g"},
                            {"name": "Curry Powder", "quantity": "2 tbsp"}
                        ],
                        "recipe": "Heat oil in a pan...",
                        "youtube_url": "https://www.youtube.com/watch?v=xxxxx"
                    }
                ],
                "scores": [0.95, 0.89, 0.82]
            }
        }

class ImageDetectionRequest(BaseModel):
    """Request model for image-based ingredient detection"""
    image: str = Field(..., description="Base64-encoded image data")
    max_meals: int = Field(default=3, ge=1, le=10, description="Number of meals to return")
    category: Optional[str] = Field(default=None, description="Filter by category")

class ImageDetectionResponse(BaseModel):
    """Response model for image-based ingredient detection"""
    detected_ingredients: List[str] = Field(..., description="List of ingredients detected in the image")
    response: str = Field(..., description="AI-generated conversational response about the meals")
    meals_used: List[Meal] = Field(..., description="List of meals found using detected ingredients")
    scores: List[float] = Field(..., description="Similarity scores for each meal")

class TextToSpeechRequest(BaseModel):
    """Request model for text-to-speech conversion"""
    text: str = Field(
        ...,
        description="Text to convert to speech",
        example="Here are some delicious chicken curry recipes..."
    )
    language: str = Field(
        default="en-US",
        description="Language code for speech generation",
        example="en-US"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Here are some delicious chicken curry recipes you can try!",
                "language": "en-US"
            }
        }

class TextToSpeechResponse(BaseModel):
    """Response model for text-to-speech conversion"""
    audio_path: str = Field(..., description="Path to the generated audio file")
    audio_url: str = Field(..., description="URL to access the audio file")
    filename: str = Field(..., description="Name of the generated audio file")
    text_length: int = Field(..., description="Length of the text that was converted")

    class Config:
        json_schema_extra = {
            "example": {
                "audio_path": "audio_output/response_1702987654.mp3",
                "audio_url": "/audio/response_1702987654.mp3",
                "filename": "response_1702987654.mp3",
                "text_length": 52
            }
        }

class WeatherRequest(BaseModel):
    """Request model for weather-based meal suggestions"""
    latitude: Optional[float] = Field(None, description="Latitude coordinate", example=40.7128)
    longitude: Optional[float] = Field(None, description="Longitude coordinate", example=-74.0060)
    location_name: Optional[str] = Field(None, description="Optional location name", example="New York")
    max_meals: int = Field(default=5, ge=1, le=10, description="Number of meals to suggest")

    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "location_name": "New York",
                "max_meals": 5
            }
        }

class WeatherResponse(BaseModel):
    """Response model for weather-based meal suggestions"""
    location: str = Field(..., description="Location name")
    temperature: float = Field(..., description="Temperature in Celsius")
    weather_condition: str = Field(..., description="Weather condition (hot/cold/rainy/etc)")
    weather_description: str = Field(..., description="Detailed weather description")
    suggestions: Dict = Field(..., description="Meal suggestions based on weather")
    recommended_meals: List[Meal] = Field(..., description="List of recommended meals for this weather")
    scores: List[float] = Field(..., description="Similarity scores for recommended meals")
    json_file: str = Field(..., description="Path to saved weather JSON data file")
    text_file: str = Field(..., description="Path to saved weather human-readable text file")
    ai_response: str = Field(..., description="AI-generated response about weather and meal suggestions")

    class Config:
        json_schema_extra = {
            "example": {
                "location": "New York",
                "temperature": 5.2,
                "weather_condition": "cold",
                "weather_description": "light snow",
                "suggestions": {
                    "recommended_categories": ["Soup", "Beef", "Pork"],
                    "recommended_keywords": ["soup", "stew", "hot", "warm"],
                    "reasoning": "It's cold outside. Warm meals will keep you cozy."
                },
                "recommended_meals": [],
                "scores": [],
                "json_file": "backend/data/weather/NewYork_20231215_143022.json",
                "text_file": "backend/data/weather/NewYork_20231215_143022.txt",
                "ai_response": "Based on the cold weather in New York..."
            }
        }

