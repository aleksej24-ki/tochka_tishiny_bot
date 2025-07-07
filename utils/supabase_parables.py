import os
import random
import psycopg2


def get_connection():
    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url:
        raise Exception("❌ SUPABASE_DB_URL не найден в переменных окружения!")
    return psycopg2.connect(db_url)


def get_random_parable():
    try:
        print("🔄 Получение случайной притчи из базы...")
        conn = get_connection()
        cur = conn.cursor()

        # Узнаём общее количество притч
        cur.execute("SELECT COUNT(*) FROM parables;")
        total = cur.fetchone()[0]

        if total == 0:
            return "❗ В базе нет ни одной притчи."

        # Выбираем случайную притчу
        offset = random.randint(0, total - 1)
        cur.execute("SELECT text FROM parables OFFSET %s LIMIT 1;", (offset,))
        result = cur.fetchone()

        if result:
            return result[0]
        else:
            return "❗ Притча не найдена."

    except Exception as e:
        print("⚠️ Ошибка при получении притчи:", e)
        return "❌ Не удалось получить притчу. Попробуй позже."

    finally:
        try:
            if conn:
                conn.close()
        except:
            pass
