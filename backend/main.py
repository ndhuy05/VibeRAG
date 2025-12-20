from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from models import (
    ChatRequest,
    ChatResponse,
    ImageDetectionRequest,
    ImageDetectionResponse,
    TextToSpeechRequest,
    TextToSpeechResponse,
    WeatherRequest,
    WeatherResponse
)
from vector_db import MealVectorDB
from data_parser import parse_all_meals
from gemini_service import GeminiService
from text_audio import TextToAudioService
from weather_service import get_weather_service
import config

# Initialize FastAPI app
app = FastAPI(
    title="Meal RAG Chat API",
    description="""
    🍳 **Meal RAG Chat API** - AI-powered cooking assistant

    This API uses **Retrieval-Augmented Generation (RAG)** with FAISS vector search and Google Gemini AI
    to help you find recipes and cooking information from a database of 570+ meals.

    ## Features
    - 🔍 Semantic search across 570+ recipes
    - 🤖 AI-generated conversational responses
    - 📝 Detailed ingredients and cooking instructions
    - 🎥 YouTube video tutorials
    - 🔊 Text-to-speech audio responses

    ## How to use
    1. Send a POST request to `/chat` with your query
    2. Get AI-generated response with relevant recipes
    3. Use the recipes to cook delicious meals!

    ## Example Query
    ```json
    {
      "query": "Find me a chicken curry recipe"
    }
    ```
    """,
    version="1.0.0",
    contact={
        "name": "Meal RAG Chat",
        "url": "https://github.com/yourusername/VibeRAG",
    },
    license_info={
        "name": "MIT",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize vector database and Gemini service
vector_db = MealVectorDB()
gemini_service = GeminiService()
tts_service = TextToAudioService()

@app.on_event("startup")
async def startup_event():
    """Load or build the FAISS index on startup"""
    print("Starting up...")
    
    # Try to load existing index
    if vector_db.load_index():
        print("Loaded existing FAISS index")
    else:
        print("No existing index found. Building new index...")
        meals = parse_all_meals()
        if meals:
            vector_db.build_index(meals)
            vector_db.save_index()
            print("Index built and saved")
        else:
            print("Warning: No meals found to index")
    
    # Mount static files for audio output
    audio_dir = "audio_output"
    if os.path.exists(audio_dir):
        app.mount("/audio", StaticFiles(directory=audio_dir), name="audio")
        print(f"Mounted audio files from {audio_dir}")

@app.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with AI about meals and recipes",
    description="""
    Send a natural language query about meals or recipes and get AI-generated responses
    with relevant meal recommendations.

    The system uses:
    - **FAISS vector search** to find semantically similar meals
    - **Google Gemini AI** to generate conversational responses
    - **570+ meal database** with detailed recipes and instructions

    You can optionally filter by category (Chicken, Beef, Vegetarian, etc.) and
    control the number of meals returned.
    """,
    response_description="AI response with relevant meals and cooking instructions",
    tags=["Chat"]
)
async def chat_with_ai(request: ChatRequest):
    """Chat endpoint - Ask anything about meals and recipes"""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    if vector_db.index is None:
        raise HTTPException(status_code=503, detail="Search index not initialized")
    
    try:
        # Extract potential ingredients from the query
        common_ingredients = [
            "chicken", "beef", "pork", "fish", "salmon", "shrimp", "tofu",
            "rice", "pasta", "noodles", "bread",
            "tomato", "onion", "garlic", "ginger", "pepper",
            "cheese", "milk", "cream", "butter", "egg",
            "coconut", "curry", "wine", "lemon", "lime"
        ]
        
        # Find ingredients mentioned in the query
        query_lower = request.query.lower()
        found_ingredients = [ing for ing in common_ingredients if ing in query_lower]
        
        # If no specific ingredients found, use the full query as search text
        if not found_ingredients:
            found_ingredients = [request.query]
        
        # Search for relevant meals
        results = vector_db.search(
            query_ingredients=found_ingredients,
            top_k=request.max_meals,
            category_filter=request.category
        )
        
        if not results:
            # No meals found - generate a simple response
            response_text = gemini_service.generate_simple_response(request.query)
            
            return ChatResponse(
                query=request.query,
                response=response_text,
                meals_used=[],
                scores=[]
            )
        
        # Extract meals and scores
        meals = [meal for meal, _ in results]
        scores = [score for _, score in results]
        
        # Generate AI response using Gemini
        response_text = gemini_service.generate_response(
            user_query=request.query,
            meals=meals,
            scores=scores
        )
        
        return ChatResponse(
            query=request.query,
            response=response_text,
            meals_used=meals,
            scores=scores
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.post("/detect-ingredients", response_model=ImageDetectionResponse)
async def detect_ingredients(request: ImageDetectionRequest):
    """
    Detect ingredients from a food image and find matching meals.
    
    Uses Gemini Vision API to analyze the image and extract ingredients,
    then searches for relevant meals using the RAG system.
    
    - **image**: Base64-encoded image data (JPEG, PNG, etc.)
    - **max_meals**: Number of meals to return (default: 3)
    - **category**: Optional filter by category
    """
    if not request.image.strip():
        raise HTTPException(status_code=400, detail="Image data cannot be empty")
    
    if vector_db.index is None:
        raise HTTPException(status_code=503, detail="Search index not initialized")
    
    try:
        # Step 1: Detect ingredients from image using Gemini Vision
        try:
            detected_ingredients = gemini_service.detect_ingredients_from_image(request.image)
        except Exception as vision_error:
            # Handle Gemini Vision API errors
            error_msg = str(vision_error)
            if "API key" in error_msg or "403" in error_msg:
                raise HTTPException(
                    status_code=503,
                    detail="Image detection service is temporarily unavailable. Please try again later or use text search instead."
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to process image: {error_msg}"
                )

        if not detected_ingredients:
            raise HTTPException(
                status_code=400,
                detail="Could not detect any ingredients in the image. Please upload a clearer food image."
            )
        
        # Step 2: Search for relevant meals using detected ingredients
        results = vector_db.search(
            query_ingredients=detected_ingredients,
            top_k=request.max_meals,
            category_filter=request.category
        )
        
        if not results:
            # No meals found - generate a simple response
            response_text = gemini_service.generate_simple_response(
                f"I detected these ingredients: {', '.join(detected_ingredients)}. "
                "However, I couldn't find any matching meals in the database."
            )
            return ImageDetectionResponse(
                detected_ingredients=detected_ingredients,
                response=response_text,
                meals_used=[],
                scores=[]
            )
        
        # Step 3: Extract meals and scores
        meals = [meal for meal, _ in results]
        scores = [score for _, score in results]
        
        # Step 4: Generate AI response using Gemini
        user_query = f"I have these ingredients: {', '.join(detected_ingredients)}. What can I make?"
        response_text = gemini_service.generate_response(
            user_query=user_query,
            meals=meals,
            scores=scores
        )
        
        return ImageDetectionResponse(
            detected_ingredients=detected_ingredients,
            response=response_text,
            meals_used=meals,
            scores=scores
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingredient detection failed: {str(e)}")
@app.post(
    "/text-to-speech",
    response_model=TextToSpeechResponse,
    summary="Convert text to speech",
    description="""
    Convert text to speech audio file. The frontend should call this endpoint
    when the user clicks the audio icon to play the response.
    
    The text will be preprocessed to remove markdown formatting and expand
    abbreviations for natural-sounding speech.
    
    Returns the path to the generated audio file which can be played immediately.
    """,
    response_description="Audio file information with path for playback",
    tags=["Text-to-Speech"]
)
async def text_to_speech(request: TextToSpeechRequest):
    """Convert text to speech on-demand"""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Generate audio from the provided text
        audio_path = tts_service.generate_audio(
            text=request.text,
            language_code=request.language
        )
        
        # Extract filename from path
        filename = os.path.basename(audio_path)
        
        # Generate URL for frontend to access the audio
        audio_url = f"/audio/{filename}"
        
        return TextToSpeechResponse(
            audio_path=audio_path,
            audio_url=audio_url,
            filename=filename,
            text_length=len(request.text)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS conversion failed: {str(e)}")

@app.post(
    "/weather-suggestions",
    response_model=WeatherResponse,
    summary="Get meal suggestions based on current weather",
    description="""
    Get personalized meal suggestions based on the current weather at a specific location.
    
    The system:
    - Fetches real-time weather data from OpenWeatherMap API
    - Saves weather data as a chunkable text file
    - Analyzes temperature and weather conditions
    - Suggests appropriate meal categories (hot soups for cold weather, light salads for hot weather, etc.)
    - Searches the meal database for matching recipes
    - Generates AI recommendations tailored to the weather
    
    Example: On a cold rainy day, you'll get warm soup and stew recommendations.
    On a hot sunny day, you'll get light salads and refreshing meals.
    """,
    response_description="Weather information with AI-recommended meals suitable for the current conditions",
    tags=["Weather"]
)
async def get_weather_based_suggestions(request: WeatherRequest):
    """Get meal suggestions based on current weather at a location"""
    
    try:
        # Get weather service instance with Gemini integration
        weather_service = get_weather_service(gemini_service)
        
        # Fetch weather data and save to files
        weather_result = weather_service.get_weather_and_save(
            lat=request.latitude,
            lon=request.longitude,
            location_name=request.location_name
        )
        
        if not weather_result:
            raise HTTPException(
                status_code=503,
                detail="Failed to fetch weather data. Please check your API key and try again."
            )
        
        weather_data = weather_result["weather_data"]
        json_file = weather_result["json_file"]
        text_file = weather_result["text_file"]
        
        # Get weather-based meal suggestions
        suggestions = weather_service.suggest_meal_categories_for_weather(weather_data)
        
        # Extract location and weather info
        location = weather_data.get("name", request.location_name or "Unknown")
        temp = weather_data.get("main", {}).get("temp", 0)
        weather_desc = weather_data.get("weather", [{}])[0].get("description", "")
        
        # Search for meals based on weather recommendations
        recommended_keywords = suggestions["recommended_keywords"]
        
        # Create a search query combining keywords
        search_query = " ".join(recommended_keywords[:3])  # Use top 3 keywords
        
        # Search for relevant meals
        results = vector_db.search(
            query_ingredients=[search_query],
            top_k=request.max_meals,
            category_filter=None
        )
        
        meals = []
        scores = []
        
        if results:
            meals = [meal for meal, _ in results]
            scores = [score for _, score in results]
        
        # Generate AI response using Gemini with weather context
        ai_response = weather_service.generate_weather_meal_response(
            weather_data=weather_data,
            meals=meals,
            scores=scores,
            location=location
        )
        
        return WeatherResponse(
            location=location,
            temperature=temp,
            weather_condition=suggestions["condition"],
            weather_description=weather_desc,
            suggestions=suggestions,
            recommended_meals=meals,
            scores=scores,
            json_file=json_file,
            text_file=text_file,
            ai_response=ai_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Weather-based suggestions failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )
