from app.core.supabase_client import supabase_
from utils import logger
from supabase import APIError

class CuentaRepository:
    def __init__(self, cliente=None):
        self.cliente = cliente or supabase_

    # --- Métodos de Usuarios ---

    async def crear_usuario(self, datos_usuario: dict): 
        # cuando se crea no se inserta el correo en la tabla correspondiente
        try:
            response = await self.cliente.table("usuarios").insert(datos_usuario).execute()
            return response.data
        except APIError as e:
            logger.error(f"Error de Supabase al crear usuario: {e.message}")
            raise RuntimeError("Error al crear usuario en la base de datos") from e

    async def obtener_dato_usuario_por_id(self, idUsuario: str, dato_requerido: str = "*"):
        try:
            response = await self.cliente.table("usuarios").select(dato_requerido).eq("id", idUsuario).execute()
            if not response.data:
                logger.warning(f"No se encontró usuario con ID {idUsuario}")
                return None
            return response.data
        except APIError as e:
            logger.error(f"Error de Supabase al obtener usuario por ID ({idUsuario}): {e.message}")
            raise RuntimeError("Error al obtener datos del usuario") from e

    async def obtener_id_y_nombre_usuario_por_correo_y_telefono(self, correo: str, telefono: str):
        try:
            response = await self.cliente.table("usuarios").select("id, nombre").eq("correo", correo).eq("numeroTelefono", telefono).execute()
            if not response.data:
                logger.warning(f"No se encontró usuario con correo {correo} y teléfono {telefono}")
                return None
            return response.data
        except APIError as e:
            logger.error(f"Error de Supabase al obtener usuario por correo y teléfono: {e.message}")
            raise RuntimeError("Error al consultar usuario") from e

    async def actualizar_usuario(self, idUsuario: str, datos_actualizados: dict):
        try:
            response = await self.cliente.table("usuarios").update(datos_actualizados).eq("id", idUsuario).execute()
            if not response.data:
                logger.warning(f"No se pudo actualizar usuario con ID {idUsuario}")
                return None
            return response.data
        except APIError as e:
            logger.error(f"Error de Supabase al actualizar usuario ({idUsuario}): {e.message}")
            raise RuntimeError("Error al actualizar usuario") from e

    async def eliminar_usuario(self, idUsuario: str):
        try:
            response = await self.cliente.table("usuarios").delete().eq("id", idUsuario).execute()
            if not response.data:
                logger.warning(f"No se pudo eliminar usuario con ID {idUsuario}")
                return None
            return response.data
        except APIError as e:
            logger.error(f"Error de Supabase al eliminar usuario ({idUsuario}): {e.message}")
            raise RuntimeError("Error al eliminar usuario") from e

    # --- Métodos de Administradores ---

    async def crear_administrador(self, datos_administrador: dict):
        try:
            response = await self.cliente.table("administradores").insert(datos_administrador).execute()
            return response.data
        except APIError as e:
            logger.error(f"Error de Supabase al crear administrador: {e.message}")
            raise RuntimeError("Error al crear administrador") from e

    async def obtener_administrador_por_id(self, idAdmin: str):
        try:
            response = await self.cliente.table("administradores").select("*").eq("id", idAdmin).execute()
            if not response.data:
                logger.warning(f"No se encontró administrador con ID {idAdmin}")
                return None
            return response.data
        except APIError as e:
            logger.error(f"Error de Supabase al obtener administrador por ID ({idAdmin}): {e.message}")
            raise RuntimeError("Error al obtener administrador") from e

    async def obtener_id_nombre_y_rol_administrador_por_correo_matricula_y_contrasena(self, correo: str, matricula: str, contrasena: str):
        try:
            response = await self.cliente.table("administradores").select("idAdmin, nombre, esSuper").eq("correo", correo).eq("matricula", matricula).eq("contrasena", contrasena).execute()
            if not response.data:
                logger.warning(f"No se encontró administrador con correo {correo} y matrícula {matricula}")
                return None
            return response.data
        except APIError as e:
            logger.error(f"Error de Supabase al obtener administrador por correo y matrícula: {e.message}")
            raise RuntimeError("Error al consultar administrador") from e

    async def eliminar_administrador(self, idAdmin: str):
        try:
            response = await self.cliente.table("administradores").delete().eq("idAdmin", idAdmin).execute()
            if not response.data:
                logger.warning(f"No se pudo eliminar administrador con ID {idAdmin}")
                return None
            return response.data
        except APIError as e:
            logger.error(f"Error de Supabase al eliminar administrador ({idAdmin}): {e.message}")
            raise RuntimeError("Error al eliminar administrador") from e
