from fastapi import APIRouter
router = APIRouter(prefix="/superadmin", tags=["Super Admin"])

@router.get("/registrar_admin")
def registrar_admin():
    
    return {"message": "Registrar nuevo administrador"}