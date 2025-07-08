import os
import random
import psycopg2


def get_connection():
    db_url = os.getenv("SUPABASE_DB_URL")
    print("📡 SUPABASE_DB_URL:", db_url)  # 👈 Добавь эту строку
    if not db_url:
        raise Exception("❌ SUPABASE_DB_URL не найден в переменных окружения!")
    return psycopg2.connect(db_url)


def get_random_parable():
    try:
        print("🔄 Получение случайной притчи из базы...")

        conn = get_connection()
        print("✅ Подключение к базе прошло успешно")

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM parables;")
        total = cur.fetchone()[0]
        print(f"📦 Найдено притч: {total}")

        if total == 0:
            print("❗ Притчи отсутствуют в базе")
            return "❗ В базе нет ни одной притчи."

        offset = random.randint(0, total - 1)
        print(f"🎯 Выбираем притчу с offset={offset}")
        cur.execute("SELECT text FROM parables OFFSET %s LIMIT 1;", (offset,))
        result = cur.fetchone()

        if result:
            print("✅ Притча найдена и возвращается")
            return result[0]
        else:
            print("❗ Притча не найдена по offset")
            return "❗ Притча не найдена."

    except Exception as e:
        print("❌ Ошибка при получении притчи:", str(e))
        return "📖❌Не удалось получить притчу. Попробуй позже."

    finally:
        try:
            if conn:
                conn.close()
                print("🔒 Соединение закрыто")
        except Exception as close_error:
            print("⚠️ Ошибка при закрытии соединения:", str(close_error))
