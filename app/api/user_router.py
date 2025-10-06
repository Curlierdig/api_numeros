from fastapi import APIRouter, Depends, HTTPException
from app.services.cuenta_service import CuentaService
from app.services.dependencias import get_cuenta_service
from models.incidencia_model import CrearIncidencia
from models.user_model import UserSession

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/estado")
async def estado():
    return {"message": "User Router funcionando"}

@router.post("/login")
async def login(
    email: str,
    password: str,
    role: str = "normal", # en el front mandaria oculto si es admin o normal
    cuenta_service: CuentaService = Depends(get_cuenta_service)
):
    token = await cuenta_service.login(email, password, role)
    if not token:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"access_token": token}

    return {"message": "Login exitoso"}

@router.post("/registrarse")
async def registrarse(usuario: UserSession):

    return {"message": "Registro exitoso"}