from app.repositories.incidencia_repository import IncidenciaRepository
from utils.logger import logger
from fastapi import HTTPException
#LOGICA DE NEGOCIO
class IncidenciaService:
    def __init__(self, db: IncidenciaRepository):
        self.db = db

    # ==============================
    # MÉTODOS DE INCIDENCIAS
    # ==============================

    async def crear_incidencia(self, datos_incidencia: dict):
        try:
            campos_requeridos = ["titulo", "descripcion", "reportado_por"]
            for campo in campos_requeridos:
                if not datos_incidencia.get(campo):
                    raise ValueError(f"El campo '{campo}' es obligatorio")

            nueva_incidencia = await self.db.crear_incidencia(datos_incidencia)

            if not nueva_incidencia:
                raise RuntimeError("Error al crear la incidencia en la base de datos")

            return nueva_incidencia

        except ValueError as ve:
            raise ve
        except Exception as e:
            raise RuntimeError(f"Error interno del servidor: {e}")

    async def obtener_incidencias_administrador(self, columna_orden: str = "fechaReporte", limite: int = 50, cursor: str = None, valor_busqueda: str = None,  ordenar_desc: bool = True):
        try:
            return await self.db.obtener_incidencias(columna_orden, limite, cursor, valor_busqueda, ordenar_desc)
        except Exception as e:
            logger.error(f"Error al obtener incidencias: {e}")
            raise HTTPException(status_code=500, detail=f"Error al obtener incidencias: {e}")
