from fastapi import Depends, HTTPException
from app.utils.auth_token import validar_token
# se usara cuando el usuario intente acceder a un area restringida
# y se necesite validar su token y rol
def requiere_admin(usuario=Depends(validar_token)):
    """funcion que valida si el usuario es admin tomando el token de la cookie"""
    if usuario["rol"] not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return usuario

def requiere_superadmin(usuario=Depends(validar_token)):
    """funcion que valida si el usuario es superadmin tomando el token de la cookie"""
    if usuario["rol"] != "superadmin":
        raise HTTPException(status_code=403, detail="Solo superadmins")
    return usuario

def requiere_normal(usuario=Depends(validar_token)):
    if usuario["rol"] != "normal":
        raise HTTPException(status_code=403, detail="Solo usuarios normales")
    return usuario
