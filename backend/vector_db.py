import faiss
import numpy as np
import json
from pathlib import Path
from typing import List, Tuple, Optional
from sentence_transformers import SentenceTransformer
from models import Meal
import config
from data_parser import create_ingredient_text

class MealVectorDB:
    """FAISS-based vector database for meal search"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the vector database.
        
        Args:
            model_name: Name of the sentence-transformer model
        """
        self.model_name = model_name or config.EMBEDDING_MODEL
        print(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        self.index: Optional[faiss.Index] = None
        self.meals: List[Meal] = []
        self.meal_texts: List[str] = []
        
    def build_index(self, meals: List[Meal]) -> None:
        """
        Build FAISS index from meals.
        
        Args:
            meals: List of Meal objects
        """
        print(f"Building index for {len(meals)} meals...")
        
        self.meals = meals
        self.meal_texts = [create_ingredient_text(meal) for meal in meals]
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.model.encode(
            self.meal_texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        # Create FAISS index (using L2 distance)
        print("Creating FAISS index...")
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Normalize vectors for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add vectors to index
        self.index.add(embeddings.astype('float32'))
        
        print(f"Index built successfully with {self.index.ntotal} vectors")
        
    def search(self, query_ingredients: List[str], top_k: int = 5, category_filter: Optional[str] = None) -> List[Tuple[Meal, float]]:
        """
        Search for meals based on ingredients.
        
        Args:
            query_ingredients: List of ingredient names
            top_k: Number of results to return
            category_filter: Optional category to filter by
            
        Returns:
            List of (Meal, score) tuples, sorted by relevance
        """
        if self.index is None or len(self.meals) == 0:
            raise ValueError("Index not initialized. Please build the index first.")
        
        # Create query text
        query_text = ", ".join(query_ingredients)
        
        # Generate query embedding
        query_embedding = self.model.encode([query_text], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        # Search in FAISS index
        # Get more results if we need to filter by category
        search_k = top_k * 3 if category_filter else top_k
        distances, indices = self.index.search(query_embedding.astype('float32'), min(search_k, len(self.meals)))
        
        # Convert distances to similarity scores (cosine similarity)
        # Since we normalized vectors, L2 distance d relates to cosine similarity as: similarity = 1 - (d^2 / 2)
        similarities = 1 - (distances[0] ** 2 / 2)
        
        results = []
        for idx, score in zip(indices[0], similarities):
            if idx < len(self.meals):
                meal = self.meals[idx]
                
                # Apply category filter if specified
                if category_filter and meal.category.lower() != category_filter.lower():
                    continue
                    
                results.append((meal, float(score)))
                
                if len(results) >= top_k:
                    break
        
        return results
    
    def save_index(self, index_path: Path = None, data_path: Path = None) -> None:
        """
        Save FAISS index and meal data to disk.
        
        Args:
            index_path: Path to save FAISS index
            data_path: Path to save meal data
        """
        if self.index is None:
            raise ValueError("No index to save")
        
        index_path = index_path or config.FAISS_INDEX_FILE
        data_path = data_path or config.MEALS_DATA_FILE
        
        # Save FAISS index
        print(f"Saving FAISS index to {index_path}")
        faiss.write_index(self.index, str(index_path))
        
        # Save meals data
        print(f"Saving meal data to {data_path}")
        meals_dict = [meal.model_dump() for meal in self.meals]
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(meals_dict, f, ensure_ascii=False, indent=2)
        
        print("Index and data saved successfully")
    
    def load_index(self, index_path: Path = None, data_path: Path = None) -> bool:
        """
        Load FAISS index and meal data from disk.
        
        Args:
            index_path: Path to FAISS index file
            data_path: Path to meal data file
            
        Returns:
            True if successful, False otherwise
        """
        index_path = index_path or config.FAISS_INDEX_FILE
        data_path = data_path or config.MEALS_DATA_FILE
        
        try:
            if not index_path.exists() or not data_path.exists():
                print("Index or data file not found")
                return False
            
            # Load FAISS index
            print(f"Loading FAISS index from {index_path}")
            self.index = faiss.read_index(str(index_path))
            
            # Load meals data
            print(f"Loading meal data from {data_path}")
            with open(data_path, 'r', encoding='utf-8') as f:
                meals_dict = json.load(f)
            
            self.meals = [Meal(**meal_data) for meal_data in meals_dict]
            self.meal_texts = [create_ingredient_text(meal) for meal in self.meals]
            
            print(f"Loaded {len(self.meals)} meals from index")
            return True
            
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def get_all_categories(self) -> List[str]:
        """Get list of all unique categories"""
        return sorted(list(set(meal.category for meal in self.meals)))
    
    def get_meals_by_category(self, category: str) -> List[Meal]:
        """Get all meals in a specific category"""
        return [meal for meal in self.meals if meal.category.lower() == category.lower()]
    
    def get_meal_by_name(self, name: str) -> Optional[Meal]:
        """Get a specific meal by name"""
        for meal in self.meals:
            if meal.name.lower() == name.lower():
                return meal
        return None

if __name__ == "__main__":
    from data_parser import parse_all_meals
    
    # Test the vector database
    print("Parsing meals...")
    meals = parse_all_meals()
    
    print("\nBuilding vector database...")
    db = MealVectorDB()
    db.build_index(meals)
    
    print("\nTesting search...")
    results = db.search(["chicken", "garlic", "coconut milk"], top_k=3)
    
    print("\nTop 3 results:")
    for meal, score in results:
        print(f"- {meal.name} ({meal.category}) - Score: {score:.3f}")
    
    print("\nSaving index...")
    db.save_index()
