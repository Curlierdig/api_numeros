from app.core.supabase_client import supabase_
from utils.logger import logger


class IncidenciaRepository:
    def __init__(self, cliente=None):
        self.cliente = cliente or supabase_
        self.tabla_incidencias = "incidencias"
        self.tabla_reportados = "reportados"
        self.tabla_destino = "destino"
        self.vista_busqueda_reportes = "mv_busqueda_reportes"  # Vista materializada para búsqueda de texto completo

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
                - esVisible (bool, opcional): Si el reporte es visible públicamente. Default True.
                - estatus (str, opcional): Estatus del reporte. Default 'pendiente
                - tipoDestino (str, opcional): Tipo de destino ('tarjeta' o 'ubicacion').
                - numeroTarjeta (str, opcional): Número de tarjeta si tipoDestino es 'tarjeta'.
                - direccion (str, opcional): Dirección si tipoDestino es 'ubicacion'.
            Retorna:
                dict: Diccionario con el mensaje de éxito y el ID del nuevo reporte.
            
            """
        try:
            numero_reportado = datos_incidencia.get("numeroReportado")

            response_numero = await self.cliente.table(self.tabla_reportados).select("idNumero").eq("numeroReportado", numero_reportado).execute()

            if not response_numero.data:
                logger.info(f"Número reportado {numero_reportado} no existe en la tabla reportados. Insertando nuevo.")
                response_numero = await self.cliente.table(self.tabla_reportados).insert({"numeroReportado": numero_reportado}).select("idNumero").execute()

            datos_reporte = {
                "idUsuario": datos_incidencia["idUsuario"],
                "idNumero": response_numero.data[0]["idNumero"],
                "categoriaReporte": datos_incidencia.get("categoriaReporte"),
                "descripcion": datos_incidencia.get("descripcion"),
                "medioContacto": datos_incidencia.get("medioContacto"),
                "genero": datos_incidencia.get("genero"),
                "supuestoNombre": datos_incidencia.get("supuestoNombre"),
                "supuestoTrabajo": datos_incidencia.get("supuestoTrabajo"),
                "esVisible": datos_incidencia.get("esVisible", True),
                "estatus": datos_incidencia.get("estatus", "pendiente")
            }

            response = await self.cliente.table(self.tabla_incidencias).insert(datos_reporte).execute()

            if not response.data:
                raise RuntimeError("No se pudo crear el reporte")

            id_reporte = response.data[0]["idReporte"]

            # 2️⃣ Insertar en destino si aplica
            tipo_destino = datos_incidencia.get("tipoDestino")
            if tipo_destino in ["tarjeta", "ubicacion"]:
                datos_destino = {
                    "tipoEnum": tipo_destino,
                    "numeroTarjeta": datos_incidencia.get("numeroTarjeta"),
                    "direccion": datos_incidencia.get("direccion"),
                    "idReporte": id_reporte
                }
                await self.cliente.table(self.tabla_destino).insert(datos_destino).execute()

            return {"mensaje": "Incidencia creada correctamente", "idReporte": id_reporte}

        except Exception as e:
            logger.error(f"Error al crear incidencia: {e}")
            raise RuntimeError("Error al crear incidencia")


    async def obtener_incidencias_para_usuario(self, limite: int = 50, ultima_fecha: str = None): #Join implicito con la tabla reportados que intercambia el nombre de la columna numeroReportado por reportados.numeroReportado
        try:
            query = await self.cliente.table(self.tabla_incidencias) \
                .select("idReporte, numeroReportado:reportados.numeroReportado, categoriaReporte, medioContacto, fechaReporte") \
                .order("fechaReporte", desc=True)
            
            if ultima_fecha:
                query = query.lt("fechaReporte", ultima_fecha)

            response = await query.limit(limite).execute()

            if response.data:
                return {
                    "data": response.data, 
                    "ultima_fecha": response.data[-1]["fechaReporte"]
                }
        except Exception as e:
            logger.error(f"Error al obtener incidencias para usuario: {e}")
            raise RuntimeError("Error al obtener incidencias para usuario")

    async def obtener_incidencias(self, columna_orden: str = "fechaReporte", limite: int = 50, cursor: str = None, valor_busqueda: str = None,  ordenar_desc: bool = True):
        """Obtiene todas las incidencias con paginación y búsqueda de texto completo.
            Parametros:
                columna_orden (str): Columna por la cual ordenar los resultados. Default es "fechaReporte".
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
            campo_combinado = "nombre_usuario || ' ' || numeroReportado || ' ' || categoriaReporte || ' ' || estatus"

            # Búsqueda por palabras + similarity
            if valor_busqueda:
                palabras = valor_busqueda.split()

                # Filtrar registros que contengan todas las palabras
                for palabra in palabras:
                    query = query.ilike(campo_combinado, f"%{palabra}%")

                # Ordenar por similarity con el texto completo
                query = query.order(f"similarity({campo_combinado}, '{valor_busqueda}')", desc=True)

            # Orden general por columna_orden
            query = query.order(columna_orden, desc=ordenar_desc)

            # Limitar resultados
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

    async def obtener_incidencia_por_id(self, idReporte: str): #aqui se debe hacer response = await supabase.table("reportes") \.select("idReporte, descripcion, categoriaReporte, destino:destino(tipoEnum, numeroTarjeta, direccion)") \.execute()
        try:
            response = await self.cliente.table(self.tabla_incidencias).select("*").eq("idReporte", idReporte).execute()
            if response.data:
                return response.data
            return None
        except Exception as e:
            logger.error(f"Error al obtener incidencia por ID {idReporte}: {e}")
            raise RuntimeError("Error al obtener incidencia por ID")


    async def actualizar_incidencia(self, idReporte: str, datos_actualizados: dict):
        try:
            response = await self.cliente.table(self.tabla_incidencias).update(datos_actualizados).eq("idReporte", idReporte).execute()
            if response.data:
                return response.data
            return None
        except Exception as e:
            logger.error(f"Error al actualizar incidencia {idReporte}: {e}")
            return None

    async def eliminar_incidencia(self, idReporte: str):
        try:
            response = await self.cliente.table(self.tabla_incidencias).delete().eq("idReporte", idReporte).execute()
            if response.data:
                return response.data
            return None
        except Exception as e:
            logger.error(f"Error al eliminar incidencia {idReporte}: {e}")
            return None

