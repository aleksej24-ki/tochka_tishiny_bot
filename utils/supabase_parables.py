import os
import psycopg2

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def get_random_parable():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT text FROM parables ORDER BY RANDOM() LIMIT 1")
            row = cur.fetchone()
            return row[0] if row else "😔 Притч пока нет."

def add_parable(text):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO parables (text) VALUES (%s)", (text,))
        conn.commit()

def count_parables():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM parables")
            return cur.fetchone()[0]
