# 🍳 Meal RAG Chat AI

AI-powered cooking assistant using RAG (Retrieval-Augmented Generation) with FAISS vector search and Google Gemini AI.

## 🚀 Quick Start

### Backend (FastAPI + FAISS + Gemini AI)

```bash
# Install dependencies
pip3 install -r backend/requirements.txt

# Run server
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

**Backend URL:** http://localhost:8001  
**API Docs:** http://localhost:8001/docs

### Frontend (Next.js + TypeScript)

```bash
# Install dependencies
cd client
npm install

# Run development server
npm run dev
```

**Frontend URL:** http://localhost:3000

## 📖 Usage

1. Open http://localhost:3000/chat
2. Ask questions like:
   - "Find me a chicken curry recipe"
   - "Món pasta Ý ngon nhất"
   - "Cách làm bánh ngọt"
3. Get AI responses with recipes, ingredients, and video tutorials

## 🔌 API Example

**Endpoint:** `POST http://localhost:8001/chat`

**Request:**
```json
{
  "query": "Find me a chicken curry recipe"
}
```

**Response:**
```json
{
  "query": "Find me a chicken curry recipe",
  "response": "Here are some delicious chicken curry recipes...",
  "meals_used": [
    {
      "name": "Chicken Curry",
      "category": "Chicken",
      "origin": "Indian",
      "ingredients": [
        {"name": "Chicken", "quantity": "500g"},
        {"name": "Curry Powder", "quantity": "2 tbsp"}
      ],
      "recipe": "Heat oil in a pan...",
      "youtube_url": "https://www.youtube.com/watch?v=xxxxx"
    }
  ],
  "scores": [0.95, 0.89, 0.82]
}
```

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Web framework
- FAISS - Vector database
- Sentence Transformers - Embeddings
- Google Gemini AI - Response generation
- PyTorch - ML framework

**Frontend:**
- Next.js 16 - React framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Shadcn/ui - UI components

## 📁 Project Structure

```
VibeRAG/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── models.py            # Pydantic models
│   ├── vector_db.py         # FAISS vector database
│   ├── gemini_service.py    # Gemini AI integration
│   └── faiss_index/         # FAISS index + 570 meals data
├── client/
│   ├── app/chat/            # Chat page
│   ├── components/chat/     # Chat components
│   ├── services/api.ts      # API service
│   └── types/chat.ts        # TypeScript types
└── README.md
```

## ✨ Features

- ✅ Semantic search across 570+ recipes
- ✅ AI-generated conversational responses
- ✅ Detailed ingredients and cooking instructions
- ✅ YouTube video tutorials
- ✅ Text-to-speech audio responses
- ✅ Category filtering (Chicken, Beef, Vegetarian, etc.)
- ✅ Responsive design
- ✅ Real-time chat interface

## 🔧 Configuration

**Backend:** Create `.env` in `backend/` folder:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

**Frontend:** `.env.local` already configured:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## 📝 API Documentation

Visit http://localhost:8001/docs for interactive Swagger documentation.

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version: `python3 --version` (need 3.8+)
- Check port 8001 is not in use

**Frontend can't connect:**
- Ensure backend is running on port 8001
- Check `.env.local` has correct API URL

**No meals returned:**
- Check FAISS index exists in `backend/faiss_index/`
- Check query is related to food/cooking

## 📄 License

MIT

