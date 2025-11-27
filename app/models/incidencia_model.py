from pydantic import BaseModel
from typing import Optional

class CrearIncidencia(BaseModel): 
    idUsuario: str 
    numeroReportado: int
    categoriaReporte: str
    descripcion: str
    medioContacto: str
    genero: Optional[str] = None
    supuestoNombre: Optional[str] = None
    supuestoTrabajo: Optional[str] = None
    tipoDestino: Optional[str] = None  # 'tarjeta' o 'ubicacion'
    numeroTarjeta: Optional[str] = None
    direccion: Optional[str] = None