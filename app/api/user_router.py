from fastapi import APIRouter, Depends, HTTPException
from ..services.cuenta_service import CuentaService
from ..services.dependencias import get_cuenta_service
from app.models.cuenta_model import UserModel

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
    try:
        token = await cuenta_service.login(email, password, role)
        if not token:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        return {"access_token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Login exitoso"}

@router.post("/registrarse")
async def registrarse(usuario: UserModel):

    return {"message": "Registro exitoso"}