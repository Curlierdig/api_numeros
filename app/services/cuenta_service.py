import re
from app.utils import logger
import uuid
from fastapi import HTTPException, status
from email_validator import validate_email, EmailNotValidError
from app.utils.hash import hashear_contrasena, confirmar_contrasena
from app.utils.auth_token import crear_token_acceso
from app.repositories.cuenta_repository import CuentaRepository
from app.models.cuenta_model import AdminModel, UserModel


class CuentaService:
    def __init__(self, db: CuentaRepository):
        self.db = db

    # ==============================
    # MÉTODOS DE ADMINISTRADORES
    # ==============================

    async def registrar_admin(self, datos_administrador: AdminModel):
        try:
            datos_administrador = datos_administrador.model_dump()
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
            #Desactivar en caso de que la matricula sea distinta a numeros y letras
            if not re.match(r"^[A-Za-z0-9]+$", datos_administrador["matricula"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La matrícula solo puede contener letras y números"
                )
            datos_administrador["contrasena"] = hashear_contrasena(datos_administrador["contrasena"])
            nuevo_admin = await self.db.crear_administrador(datos_administrador)
            if not nuevo_admin:
                raise HTTPException(
                    logger.error("Error al crear el administrador en la base de datos"),
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear el administrador en la base de datos"
                )
            return nuevo_admin
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error inesperado al registrar administrador")
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
                    logger.error("ID de administrador inválido, debe ser un UUID"),
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID de administrador inválido, debe ser un UUID"
                )
            eliminado = await self.db.eliminar_administrador(idAdmin)
            if not eliminado:
                raise HTTPException(
                    logger.error(f"No se encontró administrador con ID {idAdmin}"),
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró administrador con ID {idAdmin}"
                )
            return {"mensaje": "Administrador eliminado correctamente"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error al eliminar administrador")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {e}"
            )

    async def obtener_administradores(self, idAdmin: str):
        try:
            administrador = await self.db.obtener_administrador_por_id(idAdmin)
            if not administrador:
                raise HTTPException(
                    logger.error(f"No se encontró administrador con ID {idAdmin}"),
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró administrador con ID {idAdmin}"
                )
            return administrador
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="No se encontraron administradores con este id"
            )
    # ==============================
    # MÉTODOS DE USUARIOS
    # ==============================


    async def obtener_usuario_por_id(self, idUsuario: str, dato: str):
        try:
            usuario = await self.db.obtener_dato_usuario_por_id(idUsuario, dato)
            if not usuario:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró usuario con ID {idUsuario}"
                )
            return usuario
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error al obtener usuario por ID")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {e}"
            )

    async def registrar_usuario(self, datos_usuario: UserModel):
        usuario_existente = await self.db.verificar_existencia_usuario_por_telefono(datos_usuario.numeroTelefono)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con este número de teléfono"
            )
        try:
            datos_usuario = datos_usuario.model_dump()
            campos_requeridos = ["nombre", "edad", "sexo", "correo", "numeroTelefono", "municipio", "entidadForanea"]
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
            numero_telefono = datos_usuario["numeroTelefono"]
            if not re.match(r"^\d{10,15}$", numero_telefono):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El número de teléfono debe contener solo dígitos (10 a 15 caracteres)"
                )
            nuevo_usuario = await self.db.crear_usuario_con_correo({
                "idadmin": datos_usuario.get("idAdmin"),
                "nombre": datos_usuario["nombre"],
                "edad": datos_usuario["edad"],
                "sexo": datos_usuario["sexo"],
                "numerotelefono": datos_usuario["numeroTelefono"],
                "municipio": datos_usuario["municipio"],
                "entidadforanea": datos_usuario["entidadForanea"],
                "correo": datos_usuario["correo"]
            })
            if not nuevo_usuario:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear el usuario en la base de datos"
                )
            return nuevo_usuario
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error inesperado al registrar usuario")
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
            logger.error("Error al eliminar usuario")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {e}"
            )

    # ==============================
    # LOGIN (USUARIO Y ADMIN)
    # ==============================

    async def login(self, correo: str, contrasena: str, rol: str = "normal", matricula: str = None):
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
                    detail="El rol solo debe ser 'normal' o 'admin'"
                )
            if rol == "normal":
                usuario = await self.db.obtener_id_y_nombre_usuario_por_correo_y_telefono(correo, contrasena)
                if usuario:
                    token = crear_token_acceso(id=usuario['idusuario'], nombre=usuario['nombre'], rol="normal")
                    return token, "normal", usuario['idusuario'], None
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas para usuario normal"
                )
            if not matricula:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La matrícula es obligatoria para administradores"
                )
            contrasena_hasheada = await self.db.obtener_contrasena_administrador_por_matricula(matricula)
            if not contrasena_hasheada:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas para administrador"
                )
            contrasena_correcta = confirmar_contrasena(contrasena, contrasena_hasheada)
            if not contrasena_correcta:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas para administrador."
                )
            admin = await self.db.obtener_id_nombre_y_rol_administrador_por_correo_y_matricula(correo, matricula)
            if admin:
                rol_admin = "superadmin" if admin[0]['essuper'] else "admin"
                token = crear_token_acceso(id=admin[0]['idadmin'], nombre=admin[0]['nombre'], rol=rol_admin)
                return token, rol_admin, admin[0]['idadmin'], admin[0]['nombre']
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas para administrador"
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error en login {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {e}"
            ) from e
