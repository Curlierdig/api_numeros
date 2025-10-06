from fastapi import APIRouter
router = APIRouter(prefix="/superadmin", tags=["Super Admin"])

@router.post("/login")
def login():
    
    return {"message": "Login Super Admin exitoso"}


@router.post("/registrar_admin")
def registrar_admin():
    
    return {"message": "Registrar nuevo administrador"}

@router 

