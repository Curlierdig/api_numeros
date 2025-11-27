
from app.utils.logger import logger


class IncidenciaRepository:
    def __init__(self, cliente=None):
        self.cliente = cliente
        self.tabla_incidencias = "reportes"
        self.tabla_reportados = "reportados"
        self.tabla_destino = "destino"
        self.vista_busqueda_reportes = "mv_busqueda_reportes"  # Vista materializada para búsqueda de texto completo
        self.vista_reportes = "vista_reportes_completos"  # Vista para obtener reportes con detalles
    # ==============================
    # REPORTES / INCIDENCIAS
    # ==============================
    async def crear_incidencia(self, datos_incidencia: dict):
        """Crea una nueva incidencia y maneja la lógica de inserción en tablas relacionadas.
            Parámetros:
                datos_incidencia (dict): Diccionario con los datos de la incidencia. Debe contener:
                - idUsuario (str): ID del usuario que reporta.
                - numeroReportado (str): Número que se está reportando.
                - categoriaReporte (str): Categoría del reporte.
                - descripcion (str): Descripción del reporte.
                - medioContacto (str): Medio de contacto.
                - genero (str, opcional): Género del supuesto.
                - supuestoNombre (str, opcional): Nombre del supuesto.
                - supuestoTrabajo (str, opcional): Trabajo del supuesto.
                - estatus (str, opcional): Estatus del reporte. Default 'pendiente
                - tipoDestino (str, opcional): Tipo de destino ('tarjeta' o 'ubicacion').
                - numeroTarjeta (str, opcional): Número de tarjeta si tipoDestino es 'tarjeta'.
                - direccion (str, opcional): Dirección si tipoDestino es 'ubicacion'.
            Retorna:
                dict: Diccionario con el mensaje de éxito y el ID del nuevo reporte.    
        """
        try:
                params = {
                    "p_id_usuario": datos_incidencia["idUsuario"],
                    "p_numero_reportado": datos_incidencia["numeroReportado"],
                    "p_categoria_reporte": datos_incidencia.get("categoriaReporte"),
                    "p_descripcion": datos_incidencia.get("descripcion"),
                    "p_medio_contacto": datos_incidencia.get("medioContacto"),
                    "p_genero": datos_incidencia.get("genero"),
                    "p_supuesto_nombre": datos_incidencia.get("supuestoNombre"),
                    "p_supuesto_trabajo": datos_incidencia.get("supuestoTrabajo"),
                    "p_es_visible": datos_incidencia.get("esVisible", True),
                    "p_estatus": datos_incidencia.get("estatus", "pendiente"),
                    # Campos opcionales de destino
                    "p_tipo_destino": datos_incidencia.get("tipoDestino"),
                    "p_numero_tarjeta": datos_incidencia.get("numeroTarjeta"),
                    "p_direccion": datos_incidencia.get("direccion")
                }

                # Llamada RPC a la función creada
                response = await self.cliente.rpc("crear_incidencia_completa", params).execute()

                if not response.data:
                    raise RuntimeError("La base de datos no retornó datos.")

                return response.data

        except Exception as e:
                logger.error(f"Error al crear incidencia: {e}")
                raise RuntimeError(f"Error al crear incidencia: {str(e)}")

    async def obtener_incidencias_usuario(self, limite: int = 20, cursor: str = None): #Join implicito con la tabla reportados que intercambia el nombre de la columna numeroReportado por reportados.numeroReportado
        try:
            query = self.cliente.table(self.tabla_incidencias) \
                .select("idreporte, reportados(numeroreportado), categoriareporte, mediocontacto, fechareporte") \
                .order("fechareporte", desc=True)

            if cursor:
                query = query.lt("fechareporte", cursor)

            response = await query.limit(limite).execute()
            if response.data:
                return {
                    "data": response.data, 
                    "cursor": response.data[-1]["fechareporte"]
                }
        except Exception as e:
            logger.error(f"Error al obtener incidencias para usuario: {e}")
            raise RuntimeError("Error al obtener incidencias para usuario")

    async def obtener_incidencias(self, columna_orden: str = "fechareporte", limite: int = 50, cursor: str = None, valor_busqueda: str = None,  ordenar_desc: bool = True):
        """Obtiene todas las incidencias con paginación y búsqueda de texto completo.
            Parametros:
                columna_orden (str): Columna por la cual ordenar los resultados. Default es "fechareporte".
                limite (int): Número máximo de resultados a devolver. Default es 50.
                cursor (str): Ultimo Valor de la columna de orden para paginación. Default es None.
                valor_busqueda (str): Texto para búsqueda de texto completo. Default es None.
                ordenar_desc (bool): Indica si el orden debe ser descendente. Default es True
        """
        try:
            query = self.cliente.table("mv_busqueda_reportes").select("*")
            # Keyset pagination
            if cursor:
                if ordenar_desc:
                    query = query.lt(columna_orden, cursor)
                else: 
                    query = query.gt(columna_orden, cursor)

            # Combinación de columnas donde buscar
            campo_combinado = "nombre_usuario || ' ' || numeroreportado || ' ' || categoriareporte || ' ' || estatus"

            if valor_busqueda:
                palabras = valor_busqueda.split()
                # Filtrar registros que contengan todas las palabras
                for palabra in palabras:
                    query = query.ilike(campo_combinado, f"%{palabra}%")
                # Ordenar por similarity con el texto completo
                query = query.order(f"similarity({campo_combinado}, '{valor_busqueda}')", desc=True)

            query = query.order(columna_orden, desc=ordenar_desc)

            response = await query.limit(limite).execute()
            if response.data:
                return {
                    "data": response.data,
                    "cursor": response.data[-1][columna_orden]
                }
            return None
        except Exception as e:
            logger.error(f"Error al obtener todas las incidencias: {e}")
            raise RuntimeError("Error al obtener todas las incidencias")

    async def obtener_incidencia_por_id(self, idReporte: str):
        try:
            response = await self.cliente.table(self.vista_reportes).select("*").eq("idreporte", idReporte).execute()
            if response.data and len(response.data) > 0:
                return response.data
            return None
        except Exception as e:
            logger.error(f"Error al obtener incidencia por ID {idReporte}: {e}")
            raise RuntimeError("Error al obtener incidencia por ID")

    async def actualizar_incidencia(self, idReporte: str, datos_actualizados: dict):
        """
            Parametros:
                idReporte (str): ID del reporte a actualizar.
                datos_actualizados (dict): Diccionario con los campos a actualizar y sus nuevos valores.
                debe contener solo los campos que se desean actualizar.
                Puede incluir:
                - categoriaReporte (str): Nueva categoría del reporte.
                - descripcion (str): Nueva descripción del reporte.
                - medioContacto (str): Nuevo medio de contacto.
                - genero (str, opcional): Género del supuesto.
                - supuestoNombre (str, opcional): Nombre del supuesto.
                - supuestoTrabajo (str, opcional): Trabajo del supuesto.
                - estatus (str, opcional): Estatus del reporte. Default 'pendiente'
        """
        try:
            response = await self.cliente.table(self.tabla_incidencias).update(datos_actualizados).eq("idreporte", idReporte).execute()
            if response.data:
                return response.data
            return None
        except Exception as e:
            logger.error(f"Error al actualizar incidencia {idReporte}: {e}")
            return None
    
    async def modificar_estado_incidencia(self, idReporte: str, nuevo_estado: str):
        try:
            response = await self.cliente.table(self.tabla_incidencias).update({"estatus": nuevo_estado}).eq("idreporte", idReporte).execute()
            if response.data:
                return response.data
            return None
        except Exception as e:
            logger.error(f"Error al modificar estado de incidencia {idReporte}: {e}")
            return None

    async def eliminar_incidencia(self, idReporte: str):
        try:
            response = await self.cliente.table(self.tabla_incidencias).delete().eq("idreporte", idReporte).execute()
            if response.data:
                return response.data
            return None
        except Exception as e:
            logger.error(f"Error al eliminar incidencia {idReporte}: {e}")
            return None

