import sqlite3

DB_PATH = "users.db"

def create_parables_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS parables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_parable(text):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO parables (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def get_random_parable():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT text FROM parables ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row[0] if row else "😔 Притчи пока нет."

def get_parables_count():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM parables")
    count = cur.fetchone()[0]
    conn.close()
    return count

