from pydantic import BaseModel
from typing import Optional

class CrearIncidencia(BaseModel): #remodelar de acuerdo al modelo E-R
    telefono: int
    id_usuario: int
    id_reportado: int #cancertario
    categoria_reporte: str
    fecha_reporte: str  # Formato ISO 8601, por ejemplo, "2023-10-05T14:48:00Z"
    descripcion: str
    via: str = "Web"  # Valor por defecto no se s iborrar
    medio_contacto: str
    genero: Optional[str] = None
    supuesto_nombre: Optional[str] = None
    supuesto_trabajo: Optional[str] = None
    esVisible: bool = True #quitar talvez
    tipo_destino: str  # 'tarjeta' o 'ubicacion'
    numero_tarjeta: Optional[str] = None
    ubicacion: Optional[str] = None