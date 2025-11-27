from fastapi import APIRouter, Form, Response
from fastapi import Depends, HTTPException
from app.models.cuenta_model import UserModel
from app.services.instancias import get_cuenta_service
from app.services.cuenta_service import CuentaService
from app.utils.logger import logger

DURACION_TOKEN = 3600  # Duración del token en segundos (1 hora)

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registrar")
async def registrar(usuario: UserModel, cuenta_service: CuentaService = Depends(get_cuenta_service)):
    id = await cuenta_service.registrar_usuario(usuario)
    logger.info(f"Usuario {usuario.correo} registrado exitosamente.")
    return {"mensaje": "Usuario registrado exitosamente.", "id": id}

@router.post("/login")
async def login(
    response: Response,
    correo: str = Form(...),
    contrasena: str = Form(...), #en caso de ser usuario normal es su celular
    matricula: str = Form(None), 
    rol: str = Form("normal"), #en caso de ser admin
    cuenta_service: CuentaService = Depends(get_cuenta_service)
):
    try:
        token, rol, id = await cuenta_service.login(correo, contrasena, rol, matricula)
        if not token:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        logger.info(f"Usuario {correo} ha iniciado sesión como {rol} con token {token}")
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,  # evita acceso desde JavaScript
            max_age=DURACION_TOKEN,
            secure=False,    # solo se envía por HTTPS
            samesite="none"  # protección CSRF
        )
        return {"mensaje": "Inicio de sesión exitoso.", "rol": rol, "id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

