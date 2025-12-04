from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth_router, incidencias_router, super_admin_router, admin_router
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager
from app.core.supabase_client import crear_cliente_supabase

@asynccontextmanager
async def lifespan(app: FastAPI):
    global supabase_client
    print("Conectando a Supabase.")
    try: 
        await crear_cliente_supabase() # Se crea UNA sola vez
    except Exception as e:
        print(f"Error al conectar a Supabase: {e}")
    yield

app = FastAPI(
    title="Sistema de Registro de Números de Extorsión",
    description="API para registrar y consultar números de extorsión",
    version="1.0.0",
    lifespan=lifespan
)

# Configuración de CORS (para permitir frontend externo)
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://mi-aplicacion-frontend.com",
    "https://*.ngrok.io",
    "http://192.168.0.181:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(incidencias_router.router)
app.include_router(super_admin_router.router)
app.include_router(admin_router.router)

@app.get("/")
def root():
    return {"message": "Bienvenido al Sistema de Registro de Números de Extorsión"}

Instrumentator().instrument(app).expose(app)