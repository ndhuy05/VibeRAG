import os
import random
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("Không tìm thấy GOOGLE_API_KEY trong file .env")

genai.configure(api_key=API_KEY)

OUTPUT_DIR = r"C:\Users\PC\OneDrive\z. Coding shit\APItheMeal\Chatbot\output"

if not os.path.exists(OUTPUT_DIR):
    raise ValueError("Không tìm thấy folder output")

meals = []

for root, dirs, files in os.walk(OUTPUT_DIR):
    for f in files:
        if f.endswith(".txt"):
            meals.append(os.path.splitext(f)[0])

if not meals:
    raise ValueError("Không tìm thấy món ăn nào trong folder output")


if not meals:
    raise ValueError("Không tìm thấy món ăn nào trong folder output")

model = genai.GenerativeModel("gemini-flash-latest")

print("MealBot (Gemini)")
print("Gõ 'exit' để thoát\n")

while True:
    user_input = input("Bạn: ").strip()

    if user_input.lower() == "exit":
        break

    if user_input.lower() in ["hello", "hi", "xin chào"]:
        print("MealBot:", random.choice(meals), "\n")
        continue

    prompt = f"""
CHỈ chọn món trong danh sách sau:
{", ".join(meals)}

Câu hỏi: {user_input}
Chỉ trả lời tên món và category của món đó, và nếu người dùng bảo chỉ có số nguyên liệu đó hãy nói xin lỗi.
"""

    try:
        response = model.generate_content(prompt)
        print("MealBot:", response.text.strip(), "\n")
    except Exception as e:
        print("Gemini đang bị giới hạn quota.")
        print("MealBot (random):", random.choice(meals), "\n")
