from fastapi import APIRouter, Depends, HTTPException
from app.models.incidencia_model import CrearIncidencia
from fastapi import Query
from app.services.incidencia_service import IncidenciaService
from app.services.instancias import get_incidencia_service
from app.utils.logger import logger

router = APIRouter(prefix="/incidencias", tags=["Incidencias"])

@router.get("/filtrar_incidencias") #posibilidad de cambiar nombre
async def listar_incidencias_keyset(
    limite: int = Query(20, gt=0, le=100),
    cursor_fecha: str = Query(None),
    search_value: str = Query(None, alias="search[value]"),
    ordenar_desc: bool = Query(True),
    columna_orden: str = Query("fechaReporte"),
    incidencia_service: IncidenciaService = Depends(get_incidencia_service)
):
    result = await incidencia_service.obtener_incidencias_administrador(
        limite=limite,
        cursor=cursor_fecha,
        valor_busqueda=search_value,
        ordenar_desc=ordenar_desc,
        columna_orden=columna_orden
    )
    return result
#A BORRAR

@router.get("/incidencias_usuario")
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
async def obtener_incidencia(idReporte: str, incidencia_service: IncidenciaService = Depends(get_incidencia_service)):
    try:
        return await incidencia_service.obtener_incidencia_por_id(idReporte)
    except Exception as e:
        logger.error(f"Error al obtener incidencia {idReporte}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener incidencia: {e}")

@router.post("/crear", response_model=CrearIncidencia)
async def crear_incidencia(incidencia: CrearIncidencia, incidencia_service: IncidenciaService = Depends(get_incidencia_service)):
    resultado = await incidencia_service.crear_incidencia(incidencia)
    return resultado

@router.put("/modificar/{idReporte}")
async def modificar_incidencia(idReporte: str, incidencia: dict, incidencia_service: IncidenciaService = Depends(get_incidencia_service)):
    try:
        resultado = await incidencia_service.actualizar_incidencia(idReporte, incidencia.model_dump())
        return resultado
    except Exception as e:
        logger.error(f"Error al modificar incidencia {idReporte}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al modificar incidencia: {e}")

@router.patch("/modificar_status/{idReporte}")
async def modificar_status_incidencia(idReporte: str, nuevo_estado: str, incidencia_service: IncidenciaService = Depends(get_incidencia_service)):
    try:
        resultado = await incidencia_service.modificar_estado_incidencia(idReporte, nuevo_estado)
        return resultado
    except Exception as e:
        logger.error(f"Error al modificar estado de incidencia {idReporte}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al modificar estado de incidencia: {e}")

@router.delete("/eliminar/{idReporte}")
async def eliminar_incidencia(idReporte: str, incidencia_service: IncidenciaService = Depends(get_incidencia_service)):
    try:
        await incidencia_service.eliminar_incidencia(idReporte)
        return {"mensaje": "Incidencia eliminada exitosamente"}
    except Exception as e:
        logger.error(f"Error al eliminar incidencia {idReporte}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar incidencia: {e}")
