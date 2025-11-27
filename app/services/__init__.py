# # app/services/__init__.py
# from app.core.supabase_client import supabase_
# from app.repositories.cuenta_repository import CuentaRepository
# from app.services.cuenta_service import CuentaService

# # Singleton
# cuenta_repo = CuentaRepository(supabase_)
# cuenta_service = CuentaService(cuenta_repo)

# __all__ = ["cuenta_service", "cuenta_repo"]

# # Factory para Depends()
# _cached_service = None
# def get_cuenta_service() -> CuentaService:
#     global _cached_service
#     if _cached_service is None:
#         _cached_service = cuenta_service  # reutiliza el singleton
#     return _cached_service
