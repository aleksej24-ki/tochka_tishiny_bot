from utils.supabase_client import supabase
import random

def get_random_parable():
    try:
        response = supabase.table("parables").select("text").execute()
        data = response.data
        if not data:
            return "❗ В базе нет ни одной притчи."
        return random.choice(data)["text"]
    except Exception as e:
        print("❌ Ошибка при получении притчи:", e)
        return "📖❌ Не удалось получить притчу. Попробуй позже."
