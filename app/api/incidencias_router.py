from fastapi import APIRouter, Depends, HTTPException
from app.models.incidencia_model import CrearIncidencia
from fastapi import Query
from app.services.incidencia_service import IncidenciaService
from app.services.instancias import get_incidencia_service
from app.utils.logger import logger

router = APIRouter(prefix="/incidencias", tags=["Incidencias"])

@router.get("/filtrar") 
async def filtrar(
    limite: int = Query(20, gt=0, le=100),
    cursor_fecha: str = Query(None),
    search_value: str = Query(None, alias="search[value]"),
    orden_desc: bool = Query(True),
    columna_orden: str = Query("fechareporte"),
    incidencia_service: IncidenciaService = Depends(get_incidencia_service)
):
    resultado = await incidencia_service.obtener_incidencias_administrador(
        limite=limite,
        cursor=cursor_fecha,
        valor_busqueda=search_value,
        orden_desc=orden_desc,
        columna_orden=columna_orden
    )
    return resultado

@router.get("/usuarios")
async def listar_incidencias_usuario(
    limite: int = Query(50, gt=0, le=100),
    ultima_fecha: str = Query(None),
    incidencia_service: IncidenciaService = Depends(get_incidencia_service)
):
    try:
        return await incidencia_service.obtener_incidencias_usuario(limite, ultima_fecha)
    except Exception as e:
        logger.error(f"Error al obtener incidencias de usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener incidencias de usuario: {e}")

@router.get("/incidencia_completa/{idReporte}")
async def obtener_incidencia_completa(idReporte: str, incidencia_service: IncidenciaService = Depends(get_incidencia_service)):
    try:
        return await incidencia_service.obtener_incidencia_por_id(idReporte)
    except Exception as e:
        logger.error(f"Error al obtener incidencia {idReporte}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener incidencia: {e}")

@router.post("/crear")
async def crear_incidencia(incidencia: CrearIncidencia, 
                           incidencia_service: IncidenciaService = Depends(get_incidencia_service)):
    print(incidencia)
    resultado = await incidencia_service.crear_incidencia(incidencia)
    return resultado

@router.put("/modificar/{idReporte}")
async def modificar_incidencia(idReporte: str, incidencia: dict, 
                               incidencia_service: IncidenciaService = Depends(get_incidencia_service)):
    try:
        resultado = await incidencia_service.actualizar_incidencia(idReporte, incidencia)
        return resultado
    except Exception as e:
        logger.error(f"Error al modificar incidencia {idReporte}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al modificar incidencia: {e}")

@router.delete("/eliminar/{idReporte}")
async def eliminar_incidencia(idReporte: str, incidencia_service: IncidenciaService = Depends(get_incidencia_service)):
    try:
        await incidencia_service.eliminar_incidencia(idReporte)
        return {"mensaje": "Incidencia eliminada exitosamente"}
    except Exception as e:
        logger.error(f"Error al eliminar incidencia {idReporte}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar incidencia: {e}")
