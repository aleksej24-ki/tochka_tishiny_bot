import os
import requests
import random

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def get_random_parable():
    try:
        print("🔄 Получение случайной притчи через REST API...")

        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
        }

        # Получаем все притчи
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/parables?select=text",
            headers=headers
        )

        if response.status_code != 200:
            print("❌ Ошибка при запросе:", response.text)
            return "📖❌ Не удалось получить притчу. Попробуй позже."

        parables = response.json()
        if not parables:
            return "❗ В базе нет ни одной притчи."

        parable = random.choice(parables)
        return parable["text"]

    except Exception as e:
        print("❌ Ошибка:", str(e))
        return "📖❌ Не удалось получить притчу. Попробуй позже."
