from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Administrador"])

@router.get("/login")
def login():


    return {"message": "Lista de usuarios"}
