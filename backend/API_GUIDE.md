# Meal RAG Chat API - Usage Guide

## Quick Start

### 1. Start the API Server
```bash
python main.py
```

Server will run at: **http://localhost:8000**

---

## API Endpoints

This API provides two main endpoints:
- **`/chat`** - Get AI-generated meal recommendations
- **`/text-to-speech`** - Convert response text to audio (on-demand)

---

## Endpoint 1: Chat with AI

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

**Note:** Audio is NOT auto-generated. Use the `/text-to-speech` endpoint below to convert responses to audio.

---

## Endpoint 2: Text-to-Speech (On-Demand)

### POST /text-to-speech

Convert text responses to audio files. **Call this when the user clicks the audio icon.**

**URL:** `http://localhost:8000/text-to-speech`

**Method:** `POST`

**Request Body:**
```json
{
  "text": "Text to convert to speech",
  "language": "en-US"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | ✅ Yes | The text content to convert to speech |
| `language` | string | ❌ No | Language code (default: "en-US") |

**Response:**
```json
{
  "audio_path": "audio_output/response_1765871869.mp3",
  "audio_url": "/audio/response_1765871869.mp3",
  "filename": "response_1765871869.mp3",
  "text_length": 52
}
```

**Usage Flow:**
1. Get chat response from `/chat` endpoint
2. Display text response to user with audio icon
3. When user clicks audio icon → Send response text to `/text-to-speech`
4. Use the returned `audio_url` to play audio immediately

**Playing the Audio:**
```javascript
// Use the audio_url from the response
const audio = new Audio(`http://localhost:8000${response.audio_url}`);
audio.play();
```

---

## Usage Examples

### Chat Endpoint Examples

#### Using Python

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

#### Using JavaScript (Fetch)

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
  return data;
}

askAI("What can I make with chicken?");
```

#### Using cURL

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What can I make with chicken and garlic?", "max_meals": 3}'
```

### Text-to-Speech Examples

#### Using JavaScript (Recommended)

```javascript
async function playTextToSpeech(text) {
  try {
    // Call TTS endpoint
    const response = await fetch('http://localhost:8000/text-to-speech', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        language: 'en-US'
      })
    });
    
    const data = await response.json();
    
    // Play audio immediately
    const audio = new Audio(`http://localhost:8000${data.audio_url}`);
    await audio.play();
    
    console.log('Audio playing:', data.filename);
  } catch (error) {
    console.error('TTS Error:', error);
  }
}

// Example: Play response from chat
const chatData = await askAI("What can I make with chicken?");
playTextToSpeech(chatData.response);  // Convert response to speech
```

#### Using Python

```python
import requests

# Get chat response
chat_response = requests.post(
    "http://localhost:8000/chat",
    json={"query": "What can I make with chicken?"}
)
chat_data = chat_response.json()

# Convert response to speech
tts_response = requests.post(
    "http://localhost:8000/text-to-speech",
    json={
        "text": chat_data["response"],
        "language": "en-US"
    }
)
tts_data = tts_response.json()
print(f"Audio available at: {tts_data['audio_url']}")
```

#### Using cURL

```bash
curl -X POST "http://localhost:8000/text-to-speech" \
  -H "Content-Type: application/json" \
  -d '{"text": "Here are some chicken recipes you can try", "language": "en-US"}'
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

### Chat Response (`/chat`)

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | Your original question |
| `response` | string | AI-generated conversational answer |
| `meals_used` | array | List of meals referenced in the answer |
| `scores` | array | Relevance scores for each meal (0-1, higher is better) |

### Text-to-Speech Response (`/text-to-speech`)

| Field | Type | Description |
|-------|------|-------------|
| `audio_path` | string | Local file path to the generated audio |
| `audio_url` | string | URL to access/play the audio file |
| `filename` | string | Name of the generated audio file |
| `text_length` | integer | Number of characters converted |

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

## Frontend Integration Workflow

### Complete Implementation Example

Here's how to integrate both endpoints in your frontend:

```javascript
// 1. Get chat response
async function getChatResponse(userQuery) {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: userQuery,
      max_meals: 3
    })
  });
  return await response.json();
}

// 2. Convert response to speech (on-demand)
async function convertToSpeech(text) {
  const response = await fetch('http://localhost:8000/text-to-speech', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: text,
      language: 'en-US'
    })
  });
  return await response.json();
}

// 3. Complete workflow with UI
async function handleUserQuery(userQuery) {
  // Get AI response
  const chatData = await getChatResponse(userQuery);
  
  // Display response in UI
  displayResponse(chatData.response, chatData.meals_used);
  
  // Add audio button handler
  document.getElementById('audio-btn').addEventListener('click', async () => {
    const audioBtn = event.target;
    audioBtn.disabled = true;
    audioBtn.textContent = '⏳ Loading...';
    
    try {
      // Convert to speech
      const audioData = await convertToSpeech(chatData.response);
      
      // Play audio
      const audio = new Audio(`http://localhost:8000${audioData.audio_url}`);
      audioBtn.textContent = '▶️ Playing...';
      await audio.play();
      
      audio.onended = () => {
        audioBtn.disabled = false;
        audioBtn.textContent = '🔊 Listen';
      };
    } catch (error) {
      console.error('TTS Error:', error);
      audioBtn.disabled = false;
      audioBtn.textContent = '❌ Error';
    }
  });
}
```

### Key Points for Frontend Developers

1. **Chat Response** - No `audio_path` field anymore (removed in this version)
2. **Audio is Optional** - Only generated when user clicks the audio icon
3. **Immediate Playback** - Use `audio_url` from response to play audio right away
4. **Error Handling** - Handle both network errors and audio playback errors
5. **Loading States** - Show loading indicator while audio is being generated
6. **Static Endpoint** - Audio files served at `/audio/{filename}`

---

## How It Works

### Chat Workflow

1. **User sends question** → API extracts keywords (ingredients)
2. **FAISS searches** → Finds most similar meals from 570 recipes
3. **Context created** → Formats meal data for AI
4. **Gemini generates** → Natural language response
5. **User receives** → Conversational answer + meal details

### Text-to-Speech Workflow (Optional)

1. **User clicks audio icon** → Frontend sends response text to `/text-to-speech`
2. **Text preprocessed** → Markdown removed, abbreviations expanded
3. **gTTS converts** → Generates MP3 audio file
4. **Audio returned** → URL sent back to frontend
5. **Frontend plays** → Audio plays immediately via browser

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
