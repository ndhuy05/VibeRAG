from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Ingredient(BaseModel):
    """Ingredient model with name and quantity"""
    name: str
    quantity: str

class Meal(BaseModel):
    """Complete meal information"""
    name: str
    category: str
    origin: str
    ingredients: List[Ingredient]
    recipe: str
    youtube_url: Optional[str] = None
    
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
    """Request model for conversational chat"""
    query: str = Field(..., description="User's question or query about meals")
    max_meals: int = Field(default=3, ge=1, le=10, description="Number of meals to use as context")
    category: Optional[str] = Field(default=None, description="Filter by category")
    
class ChatResponse(BaseModel):
    """Response model for conversational chat"""
    query: str
    response: str
    meals_used: List[Meal]
    scores: List[float]
    audio_path: Optional[str] = Field(default=None, description="Path to generated audio file (if audio enabled)")
