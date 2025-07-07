import os
import random
import psycopg2

def get_connection():
    return psycopg2.connect(os.getenv("SUPABASE_DB_URL"))

def add_parable(text):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO parables (text) VALUES (%s);", (text,))
    conn.commit()
    conn.close()

def get_random_parable():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT text FROM parables ORDER BY RANDOM() LIMIT 1;")
    result = cur.fetchone()
    conn.close()
    return result[0] if result else "😔 Притчи пока нет."

def count_parables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM parables;")
    count = cur.fetchone()[0]
    conn.close()
    return count
