from fastapi import APIRouter
from app.models.incidencia_model import CrearIncidencia
from fastapi import Query


router = APIRouter(prefix="/incidencias", tags=["Incidencias"])

@router.post("/", response_model=CrearIncidencia)
async def crear_incidencia(incidencia: CrearIncidencia):
    return None

@router.get("/incidencias/keyset")
async def listar_incidencias_keyset(
    limite: int = Query(20, gt=0, le=100),
    cursor_fecha: str = Query(None),
    search_value: str = Query(None, alias="search[value]"),
    ordenar_desc: bool = Query(True),
    columna_orden: str = Query("fechaReporte"),
):
    result = await incidencia_service.obtener_incidencias_administrador(
        limite=limite,
        cursor=cursor_fecha,
        valor_busqueda=search_value,
        ordenar_desc=ordenar_desc,
        columna_orden=columna_orden
    )
    return None
#A BORRAR