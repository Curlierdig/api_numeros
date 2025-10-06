from fastapi import APIRouter
from app.services.auth_token_service import requiere_superadmin
from fastapi import Depends

router = APIRouter(prefix="/superadmin", tags=["Super Admin"])

@router.post("/login")
def login():
    
    return {"message": "Login Super Admin exitoso"}


@router.post("/registrar_admin")
def registrar_admin(usuario=Depends(requiere_superadmin)):
    return {"message": "Registrar nuevo administrador"}

@router.post("/eliminar_admin")
def eliminar_admin(usuario=Depends(requiere_superadmin)):
    return {"message": "Eliminar administrador"}
