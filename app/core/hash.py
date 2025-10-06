import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashear_contrasena(contrasena: str) -> str:
    """
    Hashea la contraseña, asegurando que no exceda el límite de 72 bytes de bcrypt.
    """
    # Pre-hash con SHA-256 para eliminar el límite de longitud
    contrasena_sha = hashlib.sha256(contrasena.encode("utf-8")).hexdigest()
    return pwd_context.hash(contrasena_sha)


def confirmar_contrasena(contrasena_plana: str, contrasena_hasheada: str) -> bool:
    """
    Verifica la contraseña hasheada, aplicando el mismo pre-hash.
    """
    contrasena_sha = hashlib.sha256(contrasena_plana.encode("utf-8")).hexdigest()
    return pwd_context.verify(contrasena_sha, contrasena_hasheada)

