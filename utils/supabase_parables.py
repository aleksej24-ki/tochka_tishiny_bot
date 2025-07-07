import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    url = os.getenv("SUPABASE_DB_URL")
    if not url:
        raise Exception("❌ SUPABASE_DB_URL не найден в переменных окружения!")
    return psycopg2.connect(url, cursor_factory=RealDictCursor)


def get_random_parable():
    try:
        print("🔄 Получение случайной притчи из базы...")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT text FROM parables ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchone()
        conn.close()
        return row["text"] if row else "😔 В базе пока нет притч."
    except Exception as e:
        print("⚠️ Ошибка при получении притчи:", e)
        return "❗️ Не удалось получить притчу. Попробуйте позже."


def add_parable(text):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO parables (text) VALUES (%s)", (text,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("⚠️ Ошибка при добавлении притчи:", e)


def count_parables():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM parables")
        count = cur.fetchone()["count"]
        conn.close()
        return count
    except Exception as e:
        print("⚠️ Ошибка при подсчёте притч:", e)
        return 0
