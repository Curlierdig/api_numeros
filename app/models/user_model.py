from pydantic import BaseModel, EmailStr

class AdminSession(BaseModel):
    nombre_completo: str
    correo: EmailStr
    numero_empleado: str
    contrasena: str
    es_super: bool = False

class UserSession(BaseModel):
    nombre_completo: str
    correo: EmailStr
    telefono: int
    edad: int
    sexo: str
    municipio: str
    entidad_foranea: str
    total_incidencias: int = 0
