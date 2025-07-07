
from utils.db import get_connection

def create_parables_table(): with get_connection() as conn: with conn.cursor() as cur: cur.execute(""" CREATE TABLE IF NOT EXISTS parables ( id SERIAL PRIMARY KEY, text TEXT NOT NULL ) """) conn.commit()

def add_parable(text): with get_connection() as conn: with conn.cursor() as cur: cur.execute("INSERT INTO parables (text) VALUES (%s)", (text,)) conn.commit()

def get_random_parable(): with get_connection() as conn: with conn.cursor() as cur: cur.execute("SELECT text FROM parables ORDER BY RANDOM() LIMIT 1") row = cur.fetchone() return row[0] if row else "😔 Притчи пока нет."

def get_parables_count(): with get_connection() as conn: with conn.cursor() as cur: cur.execute("SELECT COUNT(*) FROM parables") return cur.fetchone()[0]


