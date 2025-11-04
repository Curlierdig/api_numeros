from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Administrador"])

router.get("/dashboard")