from app.utils import logger


class CuentaRepository:
    def __init__(self, cliente=None):
        self.cliente = cliente 

    # --- Métodos de Usuarios ---
    async def insertar_correo_usuario(self, idUsuario: str, correo: str):
        try:
            response = await self.cliente.table("correos").insert({"idusuario": idUsuario, "correo": correo}).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error de Supabase al insertar correo para usuario ({idUsuario}): {str(e)}")
            raise RuntimeError("Error al insertar correo del usuario") from e

    async def crear_usuario(self, datos_usuario: dict): 
        try:
            response = await self.cliente.table("usuarios").insert(datos_usuario).execute()
            if response.data is None or len(response.data) == 0:
                logger.error("No se pudo crear el usuario, respuesta vacía de Supabase")
                raise RuntimeError("Error al crear usuario en la base de datos")
            return response.data
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
        try:
            correo_resp = await self.cliente.table("correos").select("idusuario").eq("correo", correo).execute()
            if not correo_resp.data:
                logger.warning(f"No se encontró correo {correo}")
                return None
            usuario_id = correo_resp.data[0]["idusuario"]
            usuario_resp = await self.cliente.table("usuarios").select("idusuario, nombre").eq("idusuario", usuario_id).eq("numerotelefono", telefono).execute()
            if not usuario_resp.data:
                logger.warning(f"No se encontró usuario con id {usuario_id} y teléfono {telefono}")
                return None
            return usuario_resp.data

        except Exception as e:
            logger.error(f"Error de Supabase al obtener usuario por correo y teléfono: {str(e)}")
            raise RuntimeError("Error al consultar usuario") from e

    async def verificar_existencia_usuario_por_telefono(self, telefono: str):
        try:
            response = await self.cliente.table("usuarios").select("idusuario").eq("numerotelefono", telefono).execute()
            if not response.data:
                logger.info(f"No existe usuario con teléfono {telefono}")
                return False
            return True
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

    async def obtener_id_nombre_y_rol_administrador_por_correo_matricula_y_contrasena(self, correo: str,
                                                                                       matricula: str, contrasena: str):
        try:
            response = await self.cliente.table("administradores").select("idAdmin, nombre, esSuper") \
            .eq("correo", correo).eq("matricula", matricula).eq("contrasena", contrasena).execute()
            if not response.data:
                logger.warning(f"No se encontró administrador con correo {correo} y matrícula {matricula}")
                return None
            return response.data
        except Exception as e:
            logger.error(f"Error de Supabase al obtener administrador por correo y matrícula: {str(e)}")
            raise RuntimeError("Error al consultar administrador") from e

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

