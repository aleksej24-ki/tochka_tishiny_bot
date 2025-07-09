import os
import random
from supabase import create_client, Client

# Получение данных из переменных окружения
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Проверка наличия переменных
if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise Exception("❌ Не указаны SUPABASE_URL или SUPABASE_ANON_KEY!")

# Инициализация клиента
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_random_parable():
    try:
        print("🔄 Получение притч из Supabase через API...")
        response = supabase.table("parables").select("text").execute()
        data = response.data

        if not data:
            print("❗ В Supabase нет ни одной притчи")
            return "❗ В базе нет ни одной притчи."

        parable = random.choice(data)
        print("✅ Притча выбрана случайным образом")
        return parable["text"]

    except Exception as e:
        print("❌ Ошибка при получении притчи из Supabase:", e)
        return "📖❌ Не удалось получить притчу. Попробуй позже."
