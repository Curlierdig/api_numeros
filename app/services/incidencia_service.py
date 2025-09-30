from app.repositories.incidencia_repository import IncidenciaRepository
#LOGICA DE NEGOCIO
incidencia_repo = IncidenciaRepository()
async def registrar_incidencia():
    nueva_incidencia = await incidencia_repo.create_incidencia()
    return nueva_incidencia
    