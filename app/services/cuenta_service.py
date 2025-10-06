from app.repositories.cuenta_repository import CuentaRepository
from app.core.auth_token import crear_token_acceso, verificar_token
from fastapi import HTTPException
from app.core.hash import hashear_contrasena
from email_validator import validate_email, EmailNotValidError

class CuentaService:
    def __init__(self, db: CuentaRepository):
        self.db = db

    async def registrar_admin(self, datos_administrador: dict):
        # Lógica para registrar un nuevo administrador
        try:
            validate_email(datos_administrador.get("correo"), check_deliverability=False)
            if len(datos_administrador.get("contrasena")) < 8:
                raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 8 caracteres")
            datos_administrador["contrasena"] = hashear_contrasena(datos_administrador["contrasena"])
            nuevo_admin = await self.db.crear_administrador(datos_administrador)
            return nuevo_admin
        except EmailNotValidError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def registrar_usuario(self, datos_usuario: dict):
        # Lógica para crear un nuevo usuario
        nuevo_usuario = await self.db.crear_usuario(datos_usuario)
        return nuevo_usuario

    async def login(self, correo: str, contrasena: str, rol: str, matricula: str = None):
        """
        Inicia sesión de un usuario o administrador para obtener el JWT.
        Parámetros:
            correo (str): Correo electrónico del usuario o administrador.
            matricula (str): Matrícula del administrador.
            contrasena (str): Teléfono en caso del usuario o contraseña en caso de administrador.
            rol (str): El rol es enviado desde el frontend y puede ser "normal" o "admin".
        """
        # Lógica para autenticar un usuario o administrador
        try:
            if rol == "normal":
                usuario = await self.db.obtener_id_y_nombre_usuario_por_correo_y_telefono(correo, contrasena)
                if usuario:
                    token = crear_token_acceso(id = usuario[0]['id'], name = usuario[0]['nombre'])
                    return token
                raise HTTPException(status_code=401, detail="Credenciales inválidas")
            admin = await self.db.obtener_id_nombre_y_rol_administrador_por_correo_matricula_y_contrasena(correo, matricula, hashear_contrasena(contrasena))
            if admin:
                rol = "superadmin" if admin[0].get('esSuper') else "admin"
                token = crear_token_acceso(id = admin[0]['idAdmin'], name = admin[0]['nombre'], rol = rol)
                return token
            raise HTTPException(status_code=401, detail="Sin rol válido o credenciales inválidas")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error interno del servidor: " + str(e))