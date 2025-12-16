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
    audio_path: Optional[str] = Field(None, description="Path to generated audio file (if available)")

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
                "scores": [0.95, 0.89, 0.82],
                "audio_path": "audio/response_xxxxx.mp3"
            }
        }
