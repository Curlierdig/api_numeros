import logging
from logging.handlers import RotatingFileHandler
import os

# Crear carpeta para logs si no existe
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Archivos de log
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

# Formato de logs
LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"

# Handler para logs generales
app_handler = RotatingFileHandler(
    APP_LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8"
)
app_handler.setLevel(logging.INFO)

# Handler para logs de errores
error_handler = RotatingFileHandler(
    ERROR_LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8"
)
error_handler.setLevel(logging.ERROR)

# Handler para consola (útil si corres con uvicorn o Docker)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Configurar formato
formatter = logging.Formatter(LOG_FORMAT)
app_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Crear logger principal
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Evitar duplicar handlers si el archivo se importa varias veces
if not logger.hasHandlers():
    logger.addHandler(app_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

logging.basicConfig(level=logging.DEBUG, handlers=[app_handler, error_handler, console_handler])
def error(msg: str):
    """Registra un mensaje de error usando el logger principal."""
    logger.error(msg)

def info(msg: str):
    """Registra un mensaje informativo usando el logger principal."""
    logger.info(msg)
