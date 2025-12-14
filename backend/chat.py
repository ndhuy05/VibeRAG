"""
Simple chat test script
Usage: python chat.py "your question here"
"""

import requests
import sys
import json

BASE_URL = "http://localhost:8000"

def chat(query: str, max_meals: int = 3):
    """Send a chat query to the API"""
    
    print(f"\n💬 You: {query}")
    print('─' * 60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"query": query, "max_meals": max_meals}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n🤖 AI: {data['response']}\n")
            
            if data['meals_used']:
                print(f"📊 Referenced {len(data['meals_used'])} meals:")
                for i, (meal, score) in enumerate(zip(data['meals_used'], data['scores']), 1):
                    print(f"  {i}. {meal['name']} ({meal['category']}) - {score:.1%} match")
            
            return data
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running:")
        print("   python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line usage: python chat.py "your question"
        query = " ".join(sys.argv[1:])
        chat(query)
    else:
        # Interactive mode
        print("🍳 Meal Chat - Ask me anything about meals and recipes!")
        print("Type 'quit' to exit\n")
        
        while True:
            query = input("You: ").strip()
            if not query or query.lower() in ['quit', 'exit']:
                print("👋 Goodbye!")
                break
            chat(query)
