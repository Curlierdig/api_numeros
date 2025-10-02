from fastapi import APIRouter
from models.incidencia_model import CrearIncidencia


router = APIRouter(prefix="/incidencias", tags=["Incidencias"])

@router.post("/", response_model=CrearIncidencia)
async def crear_incidencia(incidencia: CrearIncidencia):
    return None


#A BORRAR