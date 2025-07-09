from supabase import create_client
import os
import random

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_random_parable():
    try:
        response = supabase.table("parables").select("text").execute()
        data = response.data

        if not data:
            return "❗ В базе нет ни одной притчи."

        parable = random.choice(data)
        return parable["text"]

    except Exception as e:
        print("❌ Ошибка при запросе из Supabase:", e)
        return "📖❌Не удалось получить притчу. Попробуй позже."
