from app.repositories.incidencia_repository import IncidenciaRepository
#LOGICA DE NEGOCIO
incidencia = IncidenciaRepository()

async def registrar_incidencia():
    nueva_incidencia = await incidencia.crear_incidencia()
    return nueva_incidencia
    