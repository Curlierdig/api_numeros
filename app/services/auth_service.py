
from fastapi import Depends, HTTPException
from app.core.auth_token import validar_token

def requiere_admin(usuario=Depends(validar_token)):
    if usuario["role"] not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return usuario

def requiere_superadmin(usuario=Depends(validar_token)):
    if usuario["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Solo superadmins")
    return usuario

def requiere_normal(usuario=Depends(validar_token)):
    if usuario["role"] != "normal":
        raise HTTPException(status_code=403, detail="Solo usuarios normales")
    return usuario
