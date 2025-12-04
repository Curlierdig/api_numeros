from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import auth_router, incidencias_router, super_admin_router, admin_router
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager
from app.core.supabase_client import crear_cliente_supabase
from app.core.limiter import limiter
from slowapi.errors import RateLimitExceeded

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
app.state.limiter = limiter
#manejador de errores para que devuelva el 429

def rate_limit_custom_handler(request: Request, exc: RateLimitExceeded):
    """
    Atrapa el error de límite de velocidad y devuelve un JSON limpio
    que el frontend puede leer.
    """
    response = JSONResponse(
        status_code=429,
        content={
            "detail": f"Has excedido el límite de peticiones. Intenta de nuevo en unos momentos.",
            "tipo_error": "rate_limit_exceeded" # Opcional, para que el front sepa qué pasó
        }
    )
    # Esto es opcional, pero ayuda a evitar problemas de CORS en algunos navegadores
    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
    return response
app.add_exception_handler(RateLimitExceeded, rate_limit_custom_handler)

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