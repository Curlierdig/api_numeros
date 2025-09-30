# api_numeros
project/
│── app/
│   ├── api/                     # Endpoints de la API (routers)
│   │   ├── __init__.py
│   │   ├── auth.py              # Login OTP, verificación
│   │   ├── incidencias.py       # Registrar y consultar incidencias
│   │   ├── lista_negra.py       # Consultar lista negra
│   │   └── info.py              # Página de prevención/acciones
│   │
│   ├── core/                    # Configuración y utilidades
│   │   ├── __init__.py
│   │   ├── config.py            # Variables de entorno (DB, Twilio, etc.)
│   │   ├── security.py          # Generación y validación de OTP
│   │   └── dependencies.py      # Dependencias comunes
│   │
│   ├── models/                  # Modelos de BD (SQLAlchemy o Pydantic)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── incidencia.py
│   │   └── blacklist.py
│   │
│   ├── repositories/            # Patrón Repository (CRUD DB)
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── incidencia_repository.py
│   │   └── blacklist_repository.py
│   │
│   ├── services/                # Lógica de negocio (casos de uso)
│   │   ├── __init__.py
│   │   ├── auth_service.py      # Manejo OTP y validación
│   │   ├── incidencia_service.py
│   │   └── blacklist_service.py
│   │
│   ├── schemas/                 # Modelos Pydantic (validación I/O)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── incidencia.py
│   │   └── blacklist.py
│   │
│   ├── main.py                  # Punto de entrada de la aplicación
│   └── database.py              # Conexión DB y sesión
│
├── tests/                       # Pruebas unitarias
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_incidencias.py
│   └── test_blacklist.py
│
├── requirements.txt             # Dependencias (FastAPI, SQLAlchemy, Twilio)
├── .env                         # Variables de entorno (DB, API keys)
└── README.md                    # Documentación



FastAPI → service → repository → Supabase