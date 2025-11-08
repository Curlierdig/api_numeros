from fastapi import APIRouter, Depends
from app.services.incidencia_service import IncidenciaService
from app.services.instancias import get_incidencia_service
from app.models.incidencia_model import CrearIncidencia

router = APIRouter(prefix="/admin", tags=["Administrador"])

@router.get("/dashboard")
async def dashboard():
    return {"message": "Admin Router funcionando"}

