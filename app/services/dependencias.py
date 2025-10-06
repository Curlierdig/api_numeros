from repositories.cuenta_repository import CuentaRepository
from app.services.cuenta_service import CuentaService
from fastapi import Depends

def get_db_service(): 
    """Dependencia para obtener una instancia del servicio de base de datos. este solo lo llama la funcion get_cuenta_service"""
    db_service = CuentaRepository()
    try:
        yield db_service
    finally:
        pass  # Aquí podrías cerrar la conexión a la base de datos si es necesario

def get_cuenta_service(db: CuentaRepository = Depends(get_db_service)):
    """Dependencia para obtener una instancia del servicio de cuenta."""
    cuenta_service = CuentaService(db)
    return cuenta_service