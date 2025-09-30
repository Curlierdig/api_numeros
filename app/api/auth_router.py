from fastapi import APIRouter
from models.incidencia_model import CrearIncidencia
from models.user_model import UserSession


router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.get("/estado")
async def estado():
    return {"message": "Auth Router funcionando"}

@router.post("/login")

@router.post("/registrarse")
async def registrarse(usuario: UserSession):
    return {"message": "Registro exitoso"}