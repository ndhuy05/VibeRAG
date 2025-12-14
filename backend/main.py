from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import ChatRequest, ChatResponse
from vector_db import MealVectorDB
from data_parser import parse_all_meals
from gemini_service import GeminiService
import config

# Initialize FastAPI app
app = FastAPI(
    title="Meal RAG Chat API",
    description="Chat with AI about meals and recipes using RAG with FAISS",
    version="1.0.0"
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

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    Chat with AI about meals and recipes.
    
    The AI will search for relevant meals and provide a conversational response.
    
    - **query**: Your question about meals or recipes
    - **max_meals**: Number of meals to use as context (default: 3)
    - **category**: Optional filter by category
    """
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )
