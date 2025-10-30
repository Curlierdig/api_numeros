from supabase import acreate_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


async def crear_cliente_supabase() -> Client:
    return await acreate_client(SUPABASE_URL, SUPABASE_KEY)