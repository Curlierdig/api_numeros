from fastapi import APIRouter, Depends, HTTPException
from ..services.cuenta_service import CuentaService
from ..services.instancias import get_cuenta_service
from app.models.cuenta_model import UserModel

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/estado")
async def estado():

    return {"message": "User Router funcionando"}

