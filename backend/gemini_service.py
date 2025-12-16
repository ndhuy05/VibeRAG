"""
Gemini AI service for generating conversational responses based on meal data
"""

import google.generativeai as genai
from typing import List, Optional
from models import Meal
import config
import base64
from io import BytesIO
from PIL import Image

class GeminiService:
    """Service for generating AI responses using Gemini 2.5 Flash"""
    
    def __init__(self, api_key: str = None, model_name: str = None):
        """
        Initialize Gemini service
        
        Args:
            api_key: Gemini API key
            model_name: Model name (default: gemini-2.0-flash-exp)
        """
        self.api_key = api_key or config.GEMINI_API_KEY
        self.model_name = model_name or config.GEMINI_MODEL
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def create_meal_context(self, meals: List[Meal], scores: List[float]) -> str:
        """
        Create context from retrieved meals
        
        Args:
            meals: List of Meal objects
            scores: Similarity scores for each meal
            
        Returns:
            Formatted context string
        """
        context = "Here are the relevant meals I found:\n\n"
        
        for i, (meal, score) in enumerate(zip(meals, scores), 1):
            context += f"### {i}. {meal.name}\n"
            context += f"- **Category**: {meal.category}\n"
            context += f"- **Origin**: {meal.origin}\n"
            context += f"- **Relevance Score**: {score:.2%}\n"
            
            # Add ingredients
            context += f"- **Ingredients**: "
            ingredient_names = [ing.name for ing in meal.ingredients[:10]]
            context += ", ".join(ingredient_names)
            if len(meal.ingredients) > 10:
                context += f", and {len(meal.ingredients) - 10} more"
            context += "\n"
            
            # Add recipe snippet (first 200 chars)
            if meal.recipe:
                recipe_snippet = meal.recipe[:200].replace('\n', ' ').strip()
                if len(meal.recipe) > 200:
                    recipe_snippet += "..."
                context += f"- **Recipe**: {recipe_snippet}\n"
            
            if meal.youtube_url:
                context += f"- **Video Tutorial**: {meal.youtube_url}\n"
            
            context += "\n"
        
        return context
    
    def generate_response(
        self, 
        user_query: str, 
        meals: List[Meal], 
        scores: List[float]
    ) -> str:
        """
        Generate conversational response using Gemini
        
        Args:
            user_query: User's question
            meals: Retrieved meals from FAISS
            scores: Similarity scores
            
        Returns:
            AI-generated response
        """
        # Create context from retrieved meals
        context = self.create_meal_context(meals, scores)
        
        # Create prompt for Gemini
        prompt = f"""You are a helpful cooking assistant with access to a database of meal recipes. 
A user has asked you a question about meals or recipes, and I've retrieved the most relevant meals from the database.

User's Question: "{user_query}"

{context}

Based on the meals above, please provide a helpful, conversational response to the user's question. 
- If they're asking for recipe recommendations, suggest the most relevant meals and explain why they're good matches.
- If they're asking about specific ingredients, highlight meals that use those ingredients.
- If they're asking for cooking instructions, provide guidance based on the recipes.
- Include meal names, ingredients, and any relevant details from the context.
- Be friendly, concise, and helpful.
- If the user asks about YouTube links, include them in your response.

Response:"""
        
        try:
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"I encountered an error generating a response: {str(e)}\n\nHowever, I found these relevant meals based on your query:\n{context}"

    def detect_ingredients_from_image(self, image_base64: str) -> List[str]:
        """
        Detect ingredients from a food image using Gemini Vision
        
        Args:
            image_base64: Base64-encoded image data
            
        Returns:
            List of detected ingredient names
        """
        try:
            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))
            
            # Create prompt for ingredient detection
            prompt = """Analyze this food image and identify all visible ingredients.

Please list ONLY the ingredient names, one per line, without any numbering, bullets, or additional text.
Focus on the main ingredients you can clearly identify.
Be specific but concise (e.g., "chicken breast" not just "chicken").

Return only the ingredient list, nothing else."""
            
            # Generate response using Gemini Vision
            response = self.model.generate_content([prompt, image])
            
            # Parse the response to extract ingredients
            ingredients_text = response.text.strip()
            
            # Split by newlines and clean up
            ingredients = [
                ing.strip().strip('-').strip('•').strip('*').strip()
                for ing in ingredients_text.split('\n')
                if ing.strip() and not ing.strip().startswith('#')
            ]
            
            # Filter out empty strings and common non-ingredients
            ingredients = [
                ing for ing in ingredients 
                if ing and len(ing) > 1 and not ing.lower() in ['ingredients', 'list', 'item', 'items']
            ]
            
            return ingredients
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error detecting ingredients from image: {error_msg}")
            # Re-raise with more context instead of returning empty list
            if "403" in error_msg or "API key" in error_msg:
                raise Exception(f"Gemini API authentication failed: {error_msg}")
            elif "400" in error_msg:
                raise Exception(f"Invalid image format or request: {error_msg}")
            else:
                raise Exception(f"Image processing failed: {error_msg}")
    
    def generate_simple_response(self, user_query: str) -> str:
        """
        Generate response without meal context (for general questions)
        
        Args:
            user_query: User's question
            
        Returns:
            AI-generated response
        """
        prompt = f"""You are a helpful cooking assistant. A user has asked you a question.

User's Question: "{user_query}"

Please provide a helpful, conversational response. Be friendly and concise.

Response:"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I encountered an error: {str(e)}"

if __name__ == "__main__":
    # Test the Gemini service
    service = GeminiService()
    
    # Test simple response
    print("Testing simple response...")
    response = service.generate_simple_response("Hello! How can you help me?")
    print(f"Response: {response}\n")
