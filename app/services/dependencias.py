from app.repositories.cuenta_repository import CuentaRepository
from app.services.cuenta_service import CuentaService
from app.repositories.incidencia_repository import IncidenciaRepository
from fastapi import Depends
from app.services.incidencia_service import IncidenciaService
from app.core.supabase_client import crear_cliente_supabase

async def get_db_cuenta_repo(): 
    """Dependencia para obtener una instancia del repositorio de cuentas."""
    cliente = await crear_cliente_supabase()
    cuenta_repo = CuentaRepository(cliente)
    try:
        yield cuenta_repo
    finally:
        pass

async def get_db_incidencia_repo():
    cliente = await crear_cliente_supabase()
    db_incidencia = IncidenciaRepository(cliente)
    try:
        yield db_incidencia
    finally:
        pass

def get_cuenta_service(db: CuentaRepository = Depends(get_db_cuenta_repo)):
    """Dependencia para obtener una instancia del servicio de cuenta."""
    cuenta_service = CuentaService(db)
    return cuenta_service


def get_incidencia_service(db: IncidenciaRepository = Depends(get_db_incidencia_repo)):
    incidencia_service = IncidenciaService(db)
    return incidencia_service