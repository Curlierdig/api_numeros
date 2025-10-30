# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importamos los routers
from app.api import user_router, auth_router, incidencias_router, super_admin_router, admin_router

app = FastAPI(
    title="Sistema de Registro de Números de Extorsión",
    description="API para registrar y consultar números de extorsión",
    version="1.0.0",
)

# Configuración de CORS (para permitir frontend externo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar a ["http://localhost:3000"] o dominio real en producción DOMINIO NGROK
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(user_router.router) 
app.include_router(auth_router.router)
app.include_router(incidencias_router.router)
app.include_router(super_admin_router.router)
app.include_router(admin_router.router)

# Endpoint raíz
@app.get("/")
def root():
    return {"message": "Bienvenido al Sistema de Registro de Números de Extorsión"}

