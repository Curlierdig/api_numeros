from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashear_contrasena(contrasena: str) -> str:
    return pwd_context.hash(contrasena)

def confirmar_contrasena(contrasena_plana: str, contrasena_hasheada: str) -> bool:
    return pwd_context.verify(contrasena_plana, contrasena_hasheada)

