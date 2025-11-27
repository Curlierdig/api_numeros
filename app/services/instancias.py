from app.repositories.cuenta_repository import CuentaRepository
from app.services.cuenta_service import CuentaService
from app.repositories.incidencia_repository import IncidenciaRepository
from fastapi import Depends
from app.services.incidencia_service import IncidenciaService
from app.core.supabase_client import get_supabase_client

async def get_db_cuenta_repo(cliente=Depends(get_supabase_client)): 
    """Dependencia para obtener una instancia del repositorio de cuentas."""
    return CuentaRepository(cliente)


async def get_db_incidencia_repo(cliente=Depends(get_supabase_client)):
    return IncidenciaRepository(cliente)


def get_cuenta_service(db: CuentaRepository = Depends(get_db_cuenta_repo)):
    """Dependencia para obtener una instancia del servicio de cuenta."""
    return CuentaService(db)


def get_incidencia_service(db: IncidenciaRepository = Depends(get_db_incidencia_repo)):
    return IncidenciaService(db)