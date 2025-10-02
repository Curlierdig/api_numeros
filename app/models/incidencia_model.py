from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class CrearIncidencia(BaseModel): #remodelar de acuerdo al modelo E-R
    telefono: int
    id_usuario: int #en el front hara primeor un formulario para que el admin agregue al usuario y luego regrese el id para despues agregar la incidencia
    #id_reportado: int #
    numero_reportado: int #este campo no existe en la base de datos, se usa para buscar el id_reportado por medio de un trigger
    categoria_reporte: str
    fecha_reporte: str = datetime.now(timezone.utc).date().isoformat()  # Formato ISO 8601, por ejemplo, "2023-10-05T14:48:00Z"
    descripcion: str
    via: str = "Web"  # Valor por defecto no se s iborrar DE LA COOKIE INSERTAMOS ESTA
    medio_contacto: str
    genero: Optional[str] = None
    supuesto_nombre: Optional[str] = None
    supuesto_trabajo: Optional[str] = None
    tipo_destino: str  # 'tarjeta' o 'ubicacion'
    numero_tarjeta: Optional[str] = None
    ubicacion: Optional[str] = None