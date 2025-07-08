import os
import psycopg2
from datetime import datetime


def get_connection():
    db_url = os.getenv("SUPABASE_DB_URL")
    print("📡 SUPABASE_DB_URL (users):", db_url)  # 👈 Проверка
    if not db_url:
        raise Exception("❌ SUPABASE_DB_URL не найден в переменных окружения!")
    return psycopg2.connect(db_url)


def save_user(user):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                joined_at TIMESTAMP
            );
        """)
        conn.commit()

        cur.execute("SELECT id FROM users WHERE id = %s", (user.id,))
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO users (id, username, first_name, last_name, joined_at) VALUES (%s, %s, %s, %s, %s)",
                (
                    user.id,
                    user.username,
                    user.first_name,
                    user.last_name,
                    datetime.utcnow()
                )
            )
            conn.commit()
            print(f"✅ Пользователь {user.id} добавлен")
        else:
            print(f"ℹ️ Пользователь {user.id} уже существует")

    except Exception as e:
        print("❌ Ошибка при сохранении пользователя:", e)

    finally:
        try:
            if conn:
                conn.close()
                print("🔒 Соединение закрыто (users)")
        except Exception as close_error:
            print("⚠️ Ошибка при закрытии соединения:", close_error)
