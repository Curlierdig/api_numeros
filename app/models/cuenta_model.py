from pydantic import BaseModel, EmailStr

class AdminModel(BaseModel):
    nombre: str
    correo: EmailStr
    matricula: str
    contrasena: str
    essuper: bool = False

class UserModel(BaseModel):
    idAdmin: str = "578e8639-3853-471b-aa0d-8dfbcbe879d7"  # ID del administrador WEB para registro automático del usuario
    nombre: str
    correo: EmailStr
    numeroTelefono: str
    edad: int
    sexo: str
    municipio: str
    entidadForanea: str
    totalreportes: int = 0
    