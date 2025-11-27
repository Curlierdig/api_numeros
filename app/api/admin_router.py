from fastapi import APIRouter, Depends
from app.services.auth_token_service import requiere_admin
router = APIRouter(prefix="/admin", tags=["Administrador"])

@router.get("/info")
async def dashboard(usuario=Depends(requiere_admin)):
    return {"message": "Admin Router funcionando"}

