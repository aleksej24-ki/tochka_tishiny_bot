import os
import psycopg2

def get_connection():
    return psycopg2.connect(os.getenv("SUPABASE_DB_URL"))

def save_user(user):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (id, username, first_name) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;",
                (user.id, user.username, user.first_name))
    conn.commit()
    conn.close()
