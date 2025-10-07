from supabase import acreate_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase_: Client = acreate_client(SUPABASE_URL, SUPABASE_KEY)
