from fastapi import APIRouter
from models.incidencia_model import CrearIncidencia
from models.user_model import UserSession


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/estado")
async def estado():
    return {"message": "User Router funcionando"}

@router.post("/login")
async def login(
    

):
    return {"message": "Login exitoso"}

@router.post("/registrarse")
async def registrarse(usuario: UserSession):

    return {"message": "Registro exitoso"}