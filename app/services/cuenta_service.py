from app.repositories.cuenta_repository import CuentaRepository
from app.utils.auth_token import crear_token_acceso, verificar_token
from app.utils.hash import hashear_contrasena
from email_validator import validate_email, EmailNotValidError

from fastapi import HTTPException, status
from email_validator import validate_email, EmailNotValidError

class CuentaService:
    def __init__(self, db: CuentaRepository):
        self.db = db

    async def registrar_admin(self, datos_administrador: dict):
        """Lógica para registrar un nuevo administrador"""
        try:
            validate_email(datos_administrador.get("correo"), check_deliverability=False)

            if len(datos_administrador.get("contrasena", "")) < 8:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La contraseña debe tener al menos 8 caracteres"
                )

            datos_administrador["contrasena"] = hashear_contrasena(datos_administrador["contrasena"])
            nuevo_admin = await self.db.crear_administrador(datos_administrador)

            if not nuevo_admin:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear el administrador"
                )

            return nuevo_admin

        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    async def registrar_usuario(self, datos_usuario: dict):
        """Lógica para crear un nuevo usuario"""
        try:
            validate_email(datos_usuario.get("correo"), check_deliverability=False)

            if len(datos_usuario.get("telefono", "")) < 10:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El teléfono debe tener al menos 10 caracteres"
                )

            nuevo_usuario = await self.db.crear_usuario(datos_usuario)
            return nuevo_usuario

        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    async def login(self, correo: str, contrasena: str, rol: str, matricula: str = None):
        """
        Inicia sesión de un usuario o administrador para obtener el JWT.
        Parámetros:
            correo (str): Correo electrónico del usuario o administrador.
            matricula (str): Matrícula del administrador.
            contrasena (str): Teléfono en caso del usuario o contraseña en caso de administrador.
            rol (str): "normal" o "admin".
        """
        try:
            if rol == "normal":
                usuario = await self.db.obtener_id_y_nombre_usuario_por_correo_y_telefono(correo, contrasena)
                if usuario:
                    token = crear_token_acceso(id=usuario[0]['id'], name=usuario[0]['nombre'])
                    return token
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas para usuario normal"
                )

            admin = await self.db.obtener_id_nombre_y_rol_administrador_por_correo_matricula_y_contrasena(
                correo, matricula, hashear_contrasena(contrasena)
            )

            if admin:
                rol_admin = "superadmin" if admin[0].get('esSuper') else "admin"
                token = crear_token_acceso(id=admin[0]['idAdmin'], name=admin[0]['nombre'], rol=rol_admin)
                return token

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Sin rol válido o credenciales inválidas"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {e}"
            )

import re
import logging
from fastapi import HTTPException, status
from email_validator import validate_email, EmailNotValidError
from app.utils.hash import hashear_contrasena
from app.utils.auth_token import crear_token_acceso


import re
import logging
import uuid
from fastapi import HTTPException, status
from email_validator import validate_email, EmailNotValidError
from app.utils.hash import hashear_contrasena
from app.utils.auth_token import crear_token_acceso


class CuentaService:
    def __init__(self, db):
        self.db = db

    # ==============================
    # MÉTODOS DE ADMINISTRADORES
    # ==============================

    async def registrar_admin(self, datos_administrador: dict):
        try:
            campos_requeridos = ["nombre", "correo", "contrasena", "matricula"]
            for campo in campos_requeridos:
                if not datos_administrador.get(campo):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"El campo '{campo}' es obligatorio"
                    )

            try:
                validate_email(datos_administrador["correo"], check_deliverability=False)
            except EmailNotValidError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Correo inválido: {str(e)}"
                )

            if len(datos_administrador["contrasena"]) < 8:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La contraseña debe tener al menos 8 caracteres"
                )

            if not re.match(r"^[A-Za-z0-9]+$", datos_administrador["matricula"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La matrícula solo puede contener letras y números"
                )

            datos_administrador["contrasena"] = hashear_contrasena(datos_administrador["contrasena"])

            nuevo_admin = await self.db.crear_administrador(datos_administrador)

            if not nuevo_admin:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear el administrador en la base de datos"
                )

            return nuevo_admin

        except HTTPException:
            raise
        except Exception as e:
            logging.exception("Error inesperado al registrar administrador")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {e}"
            )

    async def eliminar_admin(self, idAdmin: str):
        try:
            # Validación UUID
            try:
                uuid_obj = uuid.UUID(idAdmin)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID de administrador inválido, debe ser un UUID"
                )

            eliminado = await self.db.eliminar_administrador(idAdmin)
            if not eliminado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró administrador con ID {idAdmin}"
                )

            return {"mensaje": "Administrador eliminado correctamente"}

        except HTTPException:
            raise
        except Exception as e:
            logging.exception("Error al eliminar administrador")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {e}"
            )

    # ==============================
    # MÉTODOS DE USUARIOS
    # ==============================

    async def registrar_usuario(self, datos_usuario: dict):
        try:
            campos_requeridos = ["nombre", "correo", "telefono"]
            for campo in campos_requeridos:
                if not datos_usuario.get(campo):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"El campo '{campo}' es obligatorio"
                    )

            try:
                validate_email(datos_usuario["correo"], check_deliverability=False)
            except EmailNotValidError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Correo inválido: {str(e)}"
                )

            telefono = datos_usuario["telefono"]
            if not re.match(r"^\d{10,15}$", telefono):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El teléfono debe contener solo dígitos (10 a 15 caracteres)"
                )

            nuevo_usuario = await self.db.crear_usuario(datos_usuario)
            if not nuevo_usuario:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear el usuario en la base de datos"
                )

            return nuevo_usuario

        except HTTPException:
            raise
        except Exception as e:
            logging.exception("Error inesperado al registrar usuario")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {e}"
            )

    async def eliminar_usuario(self, idUsuario: str):
        try:
            # Validación UUID
            try:
                uuid_obj = uuid.UUID(idUsuario)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID de usuario inválido, debe ser un UUID"
                )

            eliminado = await self.db.eliminar_usuario(idUsuario)
            if not eliminado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró usuario con ID {idUsuario}"
                )

            return {"mensaje": "Usuario eliminado correctamente"}

        except HTTPException:
            raise
        except Exception as e:
            logging.exception("Error al eliminar usuario")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {e}"
            )

    # ==============================
    # LOGIN (USUARIO Y ADMIN)
    # ==============================

    async def login(self, correo: str, contrasena: str, rol: str, matricula: str = None):
        try:
            if not correo or not contrasena:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Correo y contraseña/telefono son obligatorios"
                )

            try:
                validate_email(correo, check_deliverability=False)
            except EmailNotValidError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Correo electrónico inválido"
                )

            if rol not in ["normal", "admin"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El rol debe ser 'normal' o 'admin'"
                )

            if rol == "normal":
                usuario = await self.db.obtener_id_y_nombre_usuario_por_correo_y_telefono(correo, contrasena)
                if usuario:
                    token = crear_token_acceso(
                        id=usuario[0]['id'],
                        name=usuario[0]['nombre'],
                        rol="usuario"
                    )
                    return {"access_token": token, "rol": "usuario"}
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas para usuario normal"
                )

            if not matricula:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La matrícula es obligatoria para administradores"
                )

            contrasena_hasheada = hashear_contrasena(contrasena)
            admin = await self.db.obtener_id_nombre_y_rol_administrador_por_correo_matricula_y_contrasena(
                correo, matricula, contrasena_hasheada
            )

            if admin:
                rol_admin = "superadmin" if admin[0].get('esSuper') else "admin"
                token = crear_token_acceso(
                    id=admin[0]['idAdmin'],
                    name=admin[0]['nombre'],
                    rol=rol_admin
                )
                return {"access_token": token, "rol": rol_admin}

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas para administrador"
            )

        except HTTPException:
            raise
        except Exception as e:
            logging.exception("Error en login")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {e}"
            )
