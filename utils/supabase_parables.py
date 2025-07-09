import os
import random
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def get_random_parable():
    try:
        print("📡 Запрос к Supabase...")
        url = f"{SUPABASE_URL}/rest/v1/parables?select=text"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"❌ Ошибка запроса: {response.status_code}")
            return "📖📖❌Не удалось получить притчу. Попробуй позже."

        data = response.json()
        print(f"📦 Получено {len(data)} притч")
        if not data:
            return "❗ Притчи отсутствуют."

        selected = random.choice(data)
        return selected["text"]

    except Exception as e:
        print(f"❌ Ошибка при получении притчи: {e}")
        return "📖📖❌Не удалось получить притчу. Попробуй позже."
