from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import ChatRequest, ChatResponse
from vector_db import MealVectorDB
from data_parser import parse_all_meals
from gemini_service import GeminiService
from text_audio import TextToAudioService
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
            
            # Automatically generate audio from response
            try:
                audio_path = tts_service.generate_audio(response_text)
            except Exception as audio_error:
                print(f"Warning: Audio generation failed: {audio_error}")
                audio_path = None
            
            return ChatResponse(
                query=request.query,
                response=response_text,
                meals_used=[],
                scores=[],
                audio_path=audio_path
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
        
        # Automatically generate audio from response
        try:
            audio_path = tts_service.generate_audio(response_text)
        except Exception as audio_error:
            print(f"Warning: Audio generation failed: {audio_error}")
            audio_path = None
        
        return ChatResponse(
            query=request.query,
            response=response_text,
            meals_used=meals,
            scores=scores,
            audio_path=audio_path
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )
