from app.core.supabase_client import supabase
import logging
from postgrest.exceptions import APIError

from app.core.supabase_client import supabase
import logging
from postgrest.exceptions import APIError

class CuentaRepository:
    def __init__(self):
        self.cliente = supabase

    # --- Métodos de Usuarios ---

    async def crear_usuario(self, datos_usuario: dict):
        """
        Parámetros:
            datos_usuario (dict): Diccionario con los siguientes campos:
                - idUsuario: Se genera automáticamente, no es necesario enviarlo.
                - idAdmin: Identificador del administrador relacionado (opcional).
                - nombre: Nombre completo de la persona.
                - correo: Correo electrónico de la persona.
                - edad: Edad de la persona.
                - sexo: Género de la persona.
                - municipio: Municipio donde vive la persona.
                - entidadForanea: Estado donde vive la persona.
                - numeroTelefono: Número de teléfono de la persona.
                - totalReportes: Número total de reportes realizados (no es necesario enviarlo, inicia en 0).
                - fechaCreacion: Fecha de creación del usuario (se asigna automáticamente).
        
        Retorna:
            dict: Respuesta de la operación
        """
        try:
            response = self.cliente.table("usuarios").insert(datos_usuario).execute()
            return response.data
        except APIError as e:
            logging.error(f"Error de Supabase al crear usuario: {e.message}")
            raise e

    async def obtener_dato_usuario_por_id(self, idUsuario: int, dato_requerido: str = "*"):
        """
        Se obtiene el dato del usuario solicitado por su idUsuario.
        Parámetros:
            idUsuario (int): Identificador único del usuario.
            datoRequerido (str): Nombre del campo que se desea obtener. Debe estar separado por comas, sin espacios. DEFAULT: "*"
            Datos que se pueden solicitar: idAdmin, nombre, correo, edad, sexo, municipio, entidadForanea, numeroTelefono, totalReportes, fechaCreacion.

        Retorna:
            dict: Dato del usuario correspondiente al idUsuario y campo solicitado.
        """
        try:
            response = self.cliente.table("usuarios").select(dato_requerido).eq("id", idUsuario).execute()
            return response.data
        except APIError as e:
            logging.error(f"Error de Supabase al obtener usuario por ID ({idUsuario}): {e.message}")
            raise e

    async def obtener_id_y_nombre_usuario_por_correo_y_telefono(self, correo: str, telefono: str):
        """
          Parámetros:
              correo (str): Correo electrónico del usuario.
              telefono (str): Número de teléfono del usuario.
          Retorna:
              dict: Respuesta de la operación
        """
        try:
            response = self.cliente.table("usuarios").select("id, nombre").eq("correo", correo).eq("numeroTelefono", telefono).execute()
            return response.data
        except APIError as e:
            logging.error(f"Error de Supabase al obtener usuario por correo y teléfono: {e.message}")
            raise e

    async def actualizar_usuario(self, idUsuario: int, datos_actualizados: dict):
        """
        Parámetros:
            idUsuario (int): Identificador único del usuario.
            datos_actualizados (dict): Diccionario con los campos a actualizar.
            Datos que se pueden actualizar: nombre, correo, edad, sexo, municipio, entidadForanea, numeroTelefono.
            No se pueden actualizar: idUsuario, totalReportes, fechaCreacion.
        Retorna:
            dict: Respuesta de la operación
        """
        try:
            response = self.cliente.table("usuarios").update(datos_actualizados).eq("id", idUsuario).execute()
            return response.data
        except APIError as e:
            logging.error(f"Error de Supabase al actualizar usuario ({idUsuario}): {e.message}")
            raise e

    async def eliminar_usuario(self, idUsuario: int):
        try:
            response = self.cliente.table("usuarios").delete().eq("id", idUsuario).execute()
            return response.data
        except APIError as e:
            logging.error(f"Error de Supabase al eliminar usuario ({idUsuario}): {e.message}")
            raise e

    # --- Métodos de Administradores ---

    async def crear_administrador(self, datos_administrador: dict):
        """
        Parámetros:
            datos_administrador (dict): Diccionario con los siguientes campos:
                - idAdmin: Se genera automáticamente, no es necesario enviarlo.
                - nombre: Nombre completo del administrador.
                - matricula: Número de empleado del administrador.
                - correo: Correo electrónico institucional del administrador.
                - contrasena: Contraseña del administrador.
        Retorna:
            dict: Respuesta de la operación
        """
        try:
            response = self.cliente.table("administradores").insert(datos_administrador).execute()
            return response.data
        except APIError as e:
            logging.error(f"Error de Supabase al crear administrador: {e.message}")
            raise e
    
    async def obtener_administrador_por_id(self, idAdmin: int):
        """
        Parámetros:
            idAdmin (int): Identificador único del administrador.
        Retorna:
            dict: Datos del administrador correspondiente al idAdmin proporcionado.
        """
        try:
            response = self.cliente.table("administradores").select("*").eq("id", idAdmin).execute()
            return response.data
        except APIError as e:
            logging.error(f"Error de Supabase al obtener administrador por ID ({idAdmin}): {e.message}")
            raise e

    async def obtener_id_nombre_y_rol_administrador_por_correo_matricula_y_contrasena(self, correo: str, matricula: str, contrasena: str):
        """
        Parámetros:
            correo (str): Correo electrónico del administrador.
            matricula (str): Matrícula del administrador.
            contrasena (str): Contraseña del administrador.
        Retorna:
            dict: Datos del administrador correspondiente al correo y matrícula proporcionados.
        """
        try:
            response = self.cliente.table("administradores").select("idAdmin, nombre, esSuper").eq("correo", correo).eq("matricula", matricula).eq("contrasena", contrasena).execute()
            return response.data
        except APIError as e:
            logging.error(f"Error de Supabase al obtener administrador por correo y matrícula: {e.message}")
            raise e
    
    async def eliminar_administrador(self, idAdmin: int):
        """
        Parámetros:
            idAdmin (int): Identificador único del administrador.
        Retorna:
            dict: Respuesta de la operación
        """
        try:
            response = self.cliente.table("administradores").delete().eq("idAdmin", idAdmin).execute()
            return response.data
        except APIError as e:
            logging.error(f"Error de Supabase al eliminar administrador ({idAdmin}): {e.message}")
            raise e

