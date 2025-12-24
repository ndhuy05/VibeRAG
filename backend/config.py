import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
WEATHER_DATA_DIR = DATA_DIR / "weather"

# FAISS settings
FAISS_INDEX_PATH = BASE_DIR / "faiss_index"
FAISS_INDEX_FILE = FAISS_INDEX_PATH / "meal_index.faiss"
MEALS_DATA_FILE = FAISS_INDEX_PATH / "meals_data.json"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8001

# Search settings
DEFAULT_TOP_K = 5
MAX_TOP_K = 20

# Ensure directories exist
FAISS_INDEX_PATH.mkdir(exist_ok=True)

# Gemini API settings
GEMINI_API_KEY = "AIzaSyDlqC10telp1QmUozXO3OGhEvueJKWoOgE"
GEMINI_MODEL = "gemini-2.5-flash"

# OpenWeatherMap API settings
OPENWEATHER_API_KEY = "b5cf2546fbd3405ede747dfc780538c9"
# Get your free API key from: https://openweathermap.org/api
