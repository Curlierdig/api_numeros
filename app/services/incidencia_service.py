from app.repositories.incidencia_repository import IncidenciaRepository
from app.utils.logger import logger
from fastapi import HTTPException
from app.models.incidencia_model import CrearIncidencia
#LOGICA DE NEGOCIO
class IncidenciaService:
    def __init__(self, db: IncidenciaRepository):
        self.db = db

    # ==============================
    # MÉTODOS DE INCIDENCIAS
    # ==============================

    async def crear_incidencia(self, datos_incidencia: CrearIncidencia):
        """
            Parametros:
                - datos_incidencia: dict con los datos de la incidencia a crear
                Datos requeridos:
                    - idUsuario 
                    - numeroReportado
                    - categoriaReporte
                    - descripcion
                    - medioContacto
                    - genero
                    - supuestoNombre
                    - supuestoTrabajo
                    - tipoDestino
                    - numeroTarjeta
                    - direccion
        """
        try:
            campos_requeridos = ["idUsuario", "numeroReportado", "categoriaReporte", "descripcion", "medioContacto", "genero"]
            for campo in campos_requeridos:
                if not datos_incidencia.get(campo):
                    raise HTTPException(status_code=400, detail=f"El campo '{campo}' es obligatorio")

            nueva_incidencia = await self.db.crear_incidencia(datos_incidencia.model_dump())

            if not nueva_incidencia:
                raise HTTPException(status_code=500, detail="Error al crear la incidencia en la base de datos")

            return nueva_incidencia

        except ValueError as ve:
            raise ve
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

    async def obtener_incidencias_usuario(self, limite: int = 50, ultima_fecha: str = None):
        try:
            return await self.db.obtener_incidencias_usuario(limite, ultima_fecha)
        except Exception as e:
            logger.error(f"Error al obtener incidencias: {e}")
            raise HTTPException(status_code=500, detail=f"Error al obtener incidencias: {e}")

    async def obtener_incidencia_por_id(self, idReporte: str):
        if not idReporte:
            logger.error("El ID de reporte no se proporcionó")
            raise HTTPException(status_code=400, detail="El ID de reporte es obligatorio")
        try:
            return await self.db.obtener_incidencia_por_id(idReporte)
        except Exception as e:
            logger.error(f"Error al obtener incidencia por ID {idReporte}: {e}")
            raise HTTPException(status_code=500, detail=f"Error al obtener incidencia por ID: {e}")

    async def obtener_incidencias_administrador(self, columna_orden: str = "fechaReporte", limite: int = 50, cursor: str = None,
                                             valor_busqueda: str = None, orden_descendente: bool = True):
        try:
            return await self.db.obtener_incidencias(columna_orden, limite, cursor, valor_busqueda, orden_descendente)
        except Exception as e:
            logger.error(f"Error al obtener incidencias filtradas: {e}")
            raise HTTPException(status_code=500, detail=f"Error al obtener incidencias filtradas: {e}")

    async def actualizar_incidencia(self, idReporte: str, datos_actualizados: dict):
        if not idReporte:
            logger.error("El ID de reporte no se proporcionó")
            raise HTTPException(status_code=400, detail="El ID de reporte es obligatorio")
        try:
            incidencia_actualizada = await self.db.actualizar_incidencia(idReporte, datos_actualizados)
            if not incidencia_actualizada:
                raise HTTPException(status_code=404, detail="Incidencia no encontrada")
            return incidencia_actualizada
        except Exception as e:
            logger.error(f"Error al actualizar incidencia {idReporte}: {e}")
            raise HTTPException(status_code=500, detail=f"Error al actualizar incidencia: {e}")

    async def modificar_estado_incidencia(self, idReporte: str, nuevo_estado: str):
        if not idReporte:
            logger.error("El ID de reporte no se proporcionó")
            raise HTTPException(status_code=400, detail="El ID de reporte es obligatorio")
        if not nuevo_estado:
            logger.error("El nuevo estado no se proporcionó")
            raise HTTPException(status_code=400, detail="El nuevo estado es obligatorio")
        try:
            incidencia_actualizada = await self.db.modificar_estado_incidencia(idReporte, nuevo_estado)
            if not incidencia_actualizada:
                raise HTTPException(status_code=404, detail="Incidencia no encontrada")
            return incidencia_actualizada
        except Exception as e:
            logger.error(f"Error al modificar estado de incidencia {idReporte}: {e}")
            raise HTTPException(status_code=500, detail=f"Error al modificar estado de incidencia: {e}")

    async def eliminar_incidencia(self, idReporte: str):
        if not idReporte:
            logger.error("El ID de reporte no se proporcionó")
            raise HTTPException(status_code=400, detail="El ID de reporte es obligatorio")
        try:
            resultado_eliminacion = await self.db.eliminar_incidencia(idReporte)
            if not resultado_eliminacion:
                raise HTTPException(status_code=404, detail="Incidencia no encontrada")
            return {"mensaje": "Incidencia eliminada correctamente"}
        except Exception as e:
            logger.error(f"Error al eliminar incidencia {idReporte}: {e}")
            raise HTTPException(status_code=500, detail=f"Error al eliminar incidencia: {e}")