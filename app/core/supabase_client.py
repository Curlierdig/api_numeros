from supabase import acreate_client, Client
import os
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()
supabase_client: Client | None = None


async def crear_cliente_supabase():
    global supabase_client
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Faltan las variables de entorno de Supabase")
    logger.info("Creando cliente de Supabase.")
    supabase_client = await acreate_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client() -> Client:
    if supabase_client is None:
        raise RuntimeError("El cliente de Supabase no ha sido inicializado.")
    return supabase_client