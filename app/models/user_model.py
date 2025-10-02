from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone

class AdminSession(BaseModel):
    nombre_completo: str
    correo: EmailStr
    numero_empleado: str
    contrasena: str
    es_super: bool = False

class UserSession(BaseModel): #los modelos no funcionan con los formularios
    nombre_completo: str
    correo: EmailStr
    telefono: int
    edad: int
    sexo: str
    municipio: str
    entidad_foranea: str
    total_incidencias: int = 0
    fecha_registro: str = datetime.now(timezone.utc).date().isoformat()