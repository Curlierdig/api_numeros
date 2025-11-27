from fastapi import Request
from fastapi import APIRouter
from app.services.auth_token_service import requiere_superadmin
from fastapi import Depends
from app.models.cuenta_model import AdminModel
from app.services.cuenta_service import CuentaService
from app.services.instancias import get_cuenta_service
from app.utils.logger import logger

router = APIRouter(prefix="/superadmin", tags=["Super Admin"])

@router.get("/info")
def dashboard(usuario=Depends(requiere_superadmin)):
    return {"esSuperAdmin": True}

@router.post("/registrar_admin") #superadmin=Depends(requiere_superadmin),
async def registrar_admin(usuario: AdminModel, cuenta_service: CuentaService = Depends(get_cuenta_service), superadmin=Depends(requiere_superadmin)): 
    await cuenta_service.registrar_admin(usuario)
    logger.info(f"Administrador {usuario.correo} registrado exitosamente.")
    return {"mensaje": "Administrador registrado exitosamente."}

@router.post("/eliminar_admin")
def eliminar_admin(usuario=Depends(requiere_superadmin)):
    return {"message": "Eliminar administrador"}


@router.get("/cookies")
def leer_cookies(request: Request):
    return request.cookies