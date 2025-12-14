# Meal RAG Chat API - Usage Guide

## Quick Start

### 1. Start the API Server
```bash
python main.py
```

Server will run at: **http://localhost:8000**

---

## API Endpoint

### POST /chat

Ask questions about meals and get AI-powered responses.

**URL:** `http://localhost:8000/chat`

**Method:** `POST`

**Request Body:**
```json
{
  "query": "Your question here",
  "max_meals": 3,
  "category": "Chicken"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | ✅ Yes | Your question about meals or recipes |
| `max_meals` | integer | ❌ No | Number of meals to use as context (1-10, default: 3) |
| `category` | string | ❌ No | Filter by category (Beef, Chicken, Vegetarian, etc.) |

**Response:**
```json
{
  "query": "What can I make with chicken?",
  "response": "AI-generated answer with meal suggestions...",
  "meals_used": [
    {
      "name": "Honey Balsamic Chicken",
      "category": "Chicken",
      "origin": "American",
      "ingredients": [
        {"name": "Chicken Breast", "quantity": "4"},
        {"name": "Garlic", "quantity": "2 cloves"}
      ],
      "recipe": "Full recipe instructions...",
      "youtube_url": "https://youtube.com/..."
    }
  ],
  "scores": [0.901, 0.854, 0.851]
}
```

---

## Usage Examples

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "query": "What can I make with chicken and garlic?",
        "max_meals": 3
    }
)

data = response.json()
print(data["response"])  # AI's answer
print(data["meals_used"])  # Referenced meals
```

### Using JavaScript (Fetch)

```javascript
async function askAI(question) {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: question,
      max_meals: 3
    })
  });
  
  const data = await response.json();
  console.log(data.response);  // AI's answer
}

askAI("What can I make with chicken?");
```

### Using cURL

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What can I make with chicken and garlic?", "max_meals": 3}'
```

### Using the Test Script

```bash
# Command line
python chat.py "What can I make with chicken?"

# Interactive mode
python chat.py
```

---

## Example Queries

**Simple ingredient search:**
```json
{"query": "What can I make with chicken?"}
```

**Multiple ingredients:**
```json
{"query": "I have chicken, garlic, and coconut milk"}
```

**Category filter:**
```json
{
  "query": "Show me Indian dishes",
  "category": "Vegetarian"
}
```

**Get more results:**
```json
{
  "query": "What desserts do you have?",
  "max_meals": 5
}
```

---

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | Your original question |
| `response` | string | AI-generated conversational answer |
| `meals_used` | array | List of meals referenced in the answer |
| `scores` | array | Relevance scores for each meal (0-1, higher is better) |

---

## Available Categories

- Beef
- Breakfast
- Chicken
- Dessert
- Goat
- Lamb
- Miscellaneous
- Pasta
- Pork
- Seafood
- Side
- Starter
- Vegan
- Vegetarian

---

## Configuration

Edit `config.py` to customize:

```python
# Gemini API settings
GEMINI_API_KEY = "your-api-key"
GEMINI_MODEL = "gemini-2.0-flash"

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000

# Search settings
DEFAULT_TOP_K = 5
MAX_TOP_K = 20
```

---

## How It Works

1. **User sends question** → API extracts keywords (ingredients)
2. **FAISS searches** → Finds most similar meals from 570 recipes
3. **Context created** → Formats meal data for AI
4. **Gemini generates** → Natural language response
5. **User receives** → Conversational answer + meal details

---

## Troubleshooting

**Cannot connect to server:**
- Make sure server is running: `python main.py`
- Check URL: `http://localhost:8000`

**API quota exceeded:**
- Get new API key from https://aistudio.google.com/apikey
- Update `GEMINI_API_KEY` in `config.py`

**No relevant meals found:**
- Try using common ingredients
- Check available categories
- Use broader search terms

---

## CORS

CORS is enabled for all origins. The API can be called from any frontend application.

---

## Interactive API Documentation

Visit **http://localhost:8000/docs** for:
- Interactive API testing
- Request/response schemas
- Try different queries in the browser
