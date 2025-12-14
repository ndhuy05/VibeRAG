import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from models import Meal, Ingredient
import config

def parse_meal_file(file_path: Path, category: str) -> Optional[Meal]:
    """
    Parse a single meal text file and extract structured information.
    
    Args:
        file_path: Path to the meal text file
        category: Category of the meal (folder name)
        
    Returns:
        Meal object or None if parsing fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract meal name
        name_match = re.search(r'Tên món ăn:\s*(.+)', content)
        meal_name = name_match.group(1).strip() if name_match else file_path.stem
        
        # Extract origin
        origin_match = re.search(r'Nguồn Gốc:\s*(.+)', content)
        origin = origin_match.group(1).strip() if origin_match else "Unknown"
        
        # Extract ingredients section
        ingredients = []
        ingredients_section = re.search(r'Nguyên liệu:(.*?)(?=Công thức:|$)', content, re.DOTALL)
        if ingredients_section:
            ingredient_lines = ingredients_section.group(1).strip().split('\n')
            for line in ingredient_lines:
                line = line.strip()
                if ':' in line and line:
                    # Split by colon to get name and quantity
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        ing_name = parts[0].strip()
                        ing_quantity = parts[1].strip()
                        if ing_name and ing_quantity:
                            ingredients.append(Ingredient(name=ing_name, quantity=ing_quantity))
        
        # Extract recipe
        recipe_match = re.search(r'Công thức:(.*?)(?=Youtube:|$)', content, re.DOTALL)
        recipe = recipe_match.group(1).strip() if recipe_match else ""
        
        # Extract YouTube URL
        youtube_match = re.search(r'Youtube:\s*(.+)', content)
        youtube_url = youtube_match.group(1).strip() if youtube_match else None
        
        return Meal(
            name=meal_name,
            category=category,
            origin=origin,
            ingredients=ingredients,
            recipe=recipe,
            youtube_url=youtube_url
        )
    
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def parse_all_meals() -> List[Meal]:
    """
    Parse all meal files from the data directory.
    
    Returns:
        List of Meal objects
    """
    meals = []
    data_dir = config.DATA_DIR
    
    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        return meals
    
    # Iterate through category folders
    for category_dir in data_dir.iterdir():
        if category_dir.is_dir():
            category_name = category_dir.name
            print(f"Processing category: {category_name}")
            
            # Process each .txt file in the category
            for meal_file in category_dir.glob("*.txt"):
                meal = parse_meal_file(meal_file, category_name)
                if meal:
                    meals.append(meal)
    
    print(f"Total meals parsed: {len(meals)}")
    return meals

def get_ingredient_list(meal: Meal) -> List[str]:
    """
    Extract just the ingredient names from a meal.
    
    Args:
        meal: Meal object
        
    Returns:
        List of ingredient names
    """
    return [ing.name.lower() for ing in meal.ingredients]

def create_ingredient_text(meal: Meal) -> str:
    """
    Create a text representation of ingredients for embedding.
    
    Args:
        meal: Meal object
        
    Returns:
        Comma-separated ingredient names
    """
    ingredient_names = [ing.name for ing in meal.ingredients]
    return ", ".join(ingredient_names)

if __name__ == "__main__":
    # Test the parser
    meals = parse_all_meals()
    if meals:
        print(f"\nSample meal: {meals[0].name}")
        print(f"Category: {meals[0].category}")
        print(f"Origin: {meals[0].origin}")
        print(f"Ingredients: {[ing.name for ing in meals[0].ingredients]}")
