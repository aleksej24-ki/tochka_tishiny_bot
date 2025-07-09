import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("❌ SUPABASE_URL или SUPABASE_ANON_KEY не заданы")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
