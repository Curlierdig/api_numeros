from fastapi import Request, HTTPException, status
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def crear_token_acceso(id_usuario: str, nombre: str = None, rol: str = "usuario") -> dict:
    """
    Crear token de acceso JWT
    parametros:
    - id_usuario: str -> ID del usuario
    - nombre: str -> Nombre del usuario
    - rol: str -> Rol del usuario (por defecto "usuario")
    retorna: dict -> "access_token": Diccionario con el token de acceso
    """
    payload = {"sub": id_usuario, 
               "nombre": nombre,
               "rol": rol,
               "exp": datetime.now(timezone.utc) + (timedelta(minutes=30))
    }
    return {"access_token": jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)}

async def validar_token(request: Request):
    token = request.cookies.get("access_token") 
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No se proporcionó token de autenticación")            
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"id_usuario": payload["sub"], "nombre": payload["nombre"], "rol": payload["rol"]}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de autenticación ha expirado")
    
    except jwt.PyJWKError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de autenticación inválido")