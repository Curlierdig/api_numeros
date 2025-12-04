# config/limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

# Creamos la instancia aquí para poder importarla en otros lados
limiter = Limiter(key_func=get_remote_address)