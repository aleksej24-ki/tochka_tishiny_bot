import psycopg2
import os

# Прямо здесь можно вставить строку подключения:
DB_URL = os.getenv("DATABASE_URL", "postgresql://<user>:<password>@<host>:<port>/<dbname>")

def get_conn():
    return psycopg2.connect(DB_URL)

def create_table():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS parables (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL
                )
            """)
            conn.commit()

def add_parable(text):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO parables (text) VALUES (%s)", (text,))
            conn.commit()

def get_random_parable():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT text FROM parables ORDER BY RANDOM() LIMIT 1")
            result = cur.fetchone()
            return result[0] if result else "😔 Притч пока нет."

def get_parables_count():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM parables")
            return cur.fetchone()[0]