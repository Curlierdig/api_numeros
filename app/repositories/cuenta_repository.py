from app.utils import logger


class CuentaRepository:
    def __init__(self, cliente=None):
        self.cliente = cliente 

    # --- Métodos de Usuarios ---
    async def crear_usuario_con_correo(self, usuario: dict):
        try:
            response = await self.cliente.rpc(
                "crear_usuario_con_correo",
                {
                    "p_idadmin": usuario["idadmin"],
                    "p_nombre": usuario["nombre"],
                    "p_correo": usuario["correo"],
                    "p_numerotelefono": usuario["numerotelefono"],
                    "p_edad": usuario["edad"],
                    "p_sexo": usuario["sexo"],
                    "p_municipio": usuario["municipio"],
                    "p_entidadforanea": usuario["entidadforanea"],
                    "p_totalreportes": 0
                }
            ).execute()
            if response.data is None or len(response.data) == 0:
                logger.error("No se pudo crear el usuario con correo, respuesta vacía de Supabase")
                raise RuntimeError("Error al crear usuario en la base de datos")
            return "Registro exitoso"
        except Exception as e:
            logger.error(f"Error de Supabase al crear usuario: {str(e)}")
            raise RuntimeError(f"Error al crear usuario en la base de datos: {str(e)}") from e
    
    async def obtener_dato_usuario_por_id(self, idUsuario: str, dato_requerido: str = "*"):
        try:
            response = await self.cliente.table("usuarios").select(dato_requerido).eq("id", idUsuario).execute()
            if not response.data:
                logger.warning(f"No se encontró usuario con ID {idUsuario}")
                return None
            return response.data
        except Exception as e:
            logger.error(f"Error de Supabase al obtener usuario por ID ({idUsuario}): {str(e)}")
            raise RuntimeError("Error al obtener datos del usuario") from e

    async def obtener_id_y_nombre_usuario_por_correo_y_telefono(self, correo: str, telefono: str):
        """
        Verifica si existe un usuario con el correo y teléfono dados.
        """
        try:
            params = {
                "p_correo": correo,
                "p_telefono": telefono
            }
            response = await self.cliente.rpc("obtener_usuario_por_correo_y_telefono", params).execute()

            resultado = response.data 
            if not resultado:
                raise RuntimeError("La base de datos no devolvió respuesta.")

            if resultado.get("error") is True:
                logger.warning(f"Login fallido: {resultado.get('mensaje')}")
                return None 
            return resultado.get("data")

        except Exception as e:
            logger.error(f"Error crítico en repository de login: {e}")
            raise e

    async def verificar_existencia_usuario_por_telefono(self, telefono: str):
        try:
            response = await self.cliente.table("usuarios")\
            .select("idusuario", count="exact")\
            .eq("numerotelefono", telefono)\
            .limit(1)\
            .execute()
            return response.count > 0
        except Exception as e:
            logger.error(f"Error de Supabase al verificar existencia de usuario por teléfono ({telefono}): {str(e)}")
            raise RuntimeError("Error al verificar existencia de usuario") from e

    async def actualizar_usuario(self, idUsuario: str, datos_actualizados: dict):
        try:
            response = await self.cliente.table("usuarios").update(datos_actualizados).eq("id", idUsuario).execute()
            if not response.data:
                logger.warning(f"No se pudo actualizar usuario con ID {idUsuario}")
                return None
            return response.data
        except Exception as e:
            logger.error(f"Error de Supabase al actualizar usuario ({idUsuario}): {str(e)}")
            raise RuntimeError("Error al actualizar usuario") from e

    async def eliminar_usuario(self, idUsuario: str):
        try:
            response = await self.cliente.table("usuarios").delete().eq("id", idUsuario).execute()
            if not response.data:
                logger.warning(f"No se pudo eliminar usuario con ID {idUsuario}")
                return None
            return response.data
        except Exception as e:
            logger.error(f"Error de Supabase al eliminar usuario ({idUsuario}): {str(e)}")
            raise RuntimeError("Error al eliminar usuario") from e

    # --- Métodos de Administradores ---

    async def crear_administrador(self, datos_administrador: dict):
        try:
            response = await self.cliente.table("administradores").insert(datos_administrador).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error de Supabase al crear administrador: {str(e)}")
            raise RuntimeError("Error al crear administrador") from e

    async def obtener_administrador_por_id(self, idAdmin: str):
        try:
            response = await self.cliente.table("administradores").select("*").eq("id", idAdmin).execute()
            if not response.data:
                logger.warning(f"No se encontró administrador con ID {idAdmin}")
                return None
            return response.data
        except Exception as e:
            logger.error(f"Error de Supabase al obtener administrador por ID ({idAdmin}): {str(e)}")
            raise RuntimeError("Error al obtener administrador") from e

    async def obtener_id_nombre_y_rol_administrador_por_correo_y_matricula(self, correo: str,
                                                                                       matricula: str):
        try:
            response = await self.cliente.table("administradores").select("idadmin, nombre, essuper") \
            .eq("correo", correo).eq("matricula", matricula).execute()
            if not response.data:
                logger.warning(f"no info {response}")
                logger.warning(f"No se encontró administrador con correo {correo} y matrícula {matricula}")
                return None
            return response.data
        except Exception as e:
            logger.error(f"Error de Supabase al obtener administrador por correo y matrícula: {str(e)}")
            raise RuntimeError("Error al consultar administrador") from e
        
    async def obtener_contrasena_administrador_por_matricula(self, matricula: str):
        try:
            response = await self.cliente.table("administradores").select("contrasena").eq("matricula", matricula).execute()
            if not response.data[0]:
                logger.warning(f"No se encontró administrador con matrícula {matricula}")
                return None
            return response.data[0]["contrasena"]
        except Exception as e:
            logger.error(f"Error de Supabase al obtener contraseña de administrador por matrícula ({matricula}): {str(e)}")
            raise RuntimeError("Error al consultar contraseña de administrador") from e

    async def eliminar_administrador(self, idAdmin: str):
        try:
            response = await self.cliente.table("administradores").delete().eq("idAdmin", idAdmin).execute()
            if not response.data:
                logger.warning(f"No se pudo eliminar administrador con ID {idAdmin}")
                return None
            return response.data
        except Exception as e:
            logger.error(f"Error de Supabase al eliminar administrador ({idAdmin}): {str(e)}")
            raise RuntimeError("Error al eliminar administrador") from e

