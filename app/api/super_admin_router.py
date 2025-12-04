from app.core.limiter import limiter
from app.services.auth_token_service import requiere_superadmin
from fastapi import Depends, APIRouter, Request
from app.models.cuenta_model import AdminModel
from app.services.cuenta_service import CuentaService
from app.services.instancias import get_cuenta_service
from app.utils.logger import logger

router = APIRouter(prefix="/superadmin", tags=["Super Admin"])

@router.get("/info")
def dashboard(usuario=Depends(requiere_superadmin)):
    return {"esSuperAdmin": True}

@router.post("/registrar_admin") #superadmin=Depends(requiere_superadmin),
@limiter.limit("2/minute")
@limiter.limit("5/hour")
async def registrar_admin(request: Request, usuario: AdminModel, cuenta_service: CuentaService = Depends(get_cuenta_service), superadmin=Depends(requiere_superadmin)): 
    await cuenta_service.registrar_admin(usuario)
    logger.info(f"Administrador {usuario.correo} registrado exitosamente.")
    return {"mensaje": "Administrador registrado exitosamente."}

@router.post("/eliminar_admin")
@limiter.limit("2/minute")
@limiter.limit("5/hour")
def eliminar_admin(request: Request, superadmin=Depends(requiere_superadmin)):
    return {"message": "Eliminar administrador"}


@router.get("/cookies")
def leer_cookies(request: Request):
    return request.cookies