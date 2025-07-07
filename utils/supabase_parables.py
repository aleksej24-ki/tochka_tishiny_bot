import os
import psycopg2
import random


def get_connection():
    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url:
        raise ValueError("❌ SUPABASE_DB_URL не найден в переменных окружения!")
    return psycopg2.connect(db_url)


def get_random_parable():
    try:
        print("🔄 Получение случайной притчи из базы...")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT text FROM parables ORDER BY RANDOM() LIMIT 1;")
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return "❗ Притча не найдена в базе данных."
    except Exception as e:
        print("⚠️ Ошибка при получении притчи:", e)
        return "❌ Не удалось получить притчу. Попробуй позже."
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
