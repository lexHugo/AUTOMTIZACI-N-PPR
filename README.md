# Pediatría PPR - Arquitectura Limpia (Clean Architecture)

Proyecto base implementado bajo los principios de **Clean Architecture** (Arquitectura Limpia / Hexagonal) utilizando:
- **Lógica de Dominio y Aplicación:** Python puro (desacoplado de frameworks y librerías externas)
- **Procesamiento de Archivos Excel:** **Pandas** y **OpenPyXL** encapsulados en la capa de Infraestructura
- **Capa de Persistencia:** Microsoft SQL Server mediante **SQLAlchemy** y `pyodbc`
- **Capa de Presentación / Entrada:** **FastAPI** (con esquemas Pydantic, subida/descarga de archivos y documentación Swagger/OpenAPI)

---

## 🏛️ Estructura del Proyecto

El proyecto sigue la regla fundamental de Clean Architecture: **las capas internas no conocen a las capas externas**. Los casos de uso dependen de puertos abstractos (`PatientExcelPort`, `PatientRepositoryInterface`), mientras que Pandas y SQLAlchemy son simples adaptadores intercambiables en la infraestructura.

```
PEDIATRIA_PPR/
│
├── app/
│   │
│   ├── domain/                         # CAPA DE DOMINIO (Reglas de negocio puras)
│   │   ├── entities/patient.py         # Entidad Patient (cálculo de edad, validación pediátrica)
│   │   ├── repositories/               # Contratos abstractos de persistencia
│   │   │   └── patient_repository.py  # PatientRepositoryInterface (ABC)
│   │   └── exceptions/                 # Excepciones de negocio
│   │       └── domain_exceptions.py
│   │
│   ├── application/                    # CAPA DE APLICACIÓN (Casos de uso)
│   │   ├── dtos/patient_dto.py         # DTOs de entrada, salida y resultado de importación
│   │   ├── ports/                      # Puertos de salida (interfaces abstractas)
│   │   │   └── patient_excel_port.py  # PatientExcelPort (ABC)
│   │   └── use_cases/                  # Casos de uso específicos
│   │       ├── create_patient.py       # Registrar paciente
│   │       ├── get_patient.py          # Consultar paciente por ID
│   │       ├── list_patients.py        # Listar pacientes
│   │       ├── export_patients_excel.py # Exportar pacientes a .xlsx
│   │       ├── import_patients_excel.py # Importar masivamente desde .xlsx con validaciones
│   │       └── generate_patient_template.py # Generar plantilla oficial descargable
│   │
│   ├── infrastructure/                 # CAPA DE INFRAESTRUCTURA (Herramientas y adaptadores)
│   │   ├── config/settings.py          # Variables de entorno y connection string SQL Server
│   │   ├── database/session.py         # Sesión y Engine SQLAlchemy
│   │   ├── models/patient_model.py     # Modelo ORM mapeado a SQL Server
│   │   ├── repositories/               # Implementación concreta del repositorio
│   │   │   └── sqlalchemy_patient_repository.py
│   │   └── services/                   # Adaptadores de servicios externos
│   │       └── pandas_patient_excel_service.py # Implementación con Pandas y OpenPyXL
│   │
│   └── presentation/                   # CAPA DE PRESENTACIÓN / ENTRADA (FastAPI)
│       ├── api/
│       │   ├── dependencies.py         # Inyección de dependencias (DI)
│       │   └── v1/
│       │       ├── router.py           # Agrupador de rutas API v1
│       │       └── endpoints/
│       │           └── patients.py     # Endpoints CRUD y de importación/exportación Excel
│       └── schemas/
│           ├── patient_schema.py       # Modelos Pydantic de pacientes
│           └── excel_schema.py         # Modelo Pydantic para el resumen de importación
│
├── main.py                             # Punto de entrada de la aplicación FastAPI
├── requirements.txt                    # Dependencias del proyecto
├── .env.example                        # Ejemplo de configuración
└── README.md                           # Documentación técnica
```

---

## 📊 Módulo de Hojas de Cálculo con Pandas

El procesamiento de Excel está desacoplado mediante el puerto [`PatientExcelPort`](file:///C:/Users/hugo_/Desktop/PEDIATRIA_PPR/app/application/ports/patient_excel_port.py):

1. **Exportación a Excel (`GET /api/v1/patients/export/excel`):**
   - Extrae los pacientes de la base de datos SQL Server.
   - Genera dinámicamente un archivo `.xlsx` en memoria (`io.BytesIO`) utilizando **Pandas** y **OpenPyXL**.
   - Incluye auto-ajuste de ancho de columnas y cabeceras descriptivas en español.
   - Se descarga como archivo adjunto (`Content-Disposition: attachment`).

2. **Importación Masiva desde Excel (`POST /api/v1/patients/import/excel`):**
   - Recibe un archivo `.xlsx` subido vía `multipart/form-data`.
   - Pandas procesa las filas, normaliza los nombres de columna y valida los formatos de fecha.
   - El caso de uso evalúa fila por fila:
     - Unicidad de historia clínica.
     - Límite de edad pediátrica (< 18 años).
   - Retorna un resumen con el total de filas, cantidad exitosa, cantidad fallida y lista de errores detallada por número de fila.

3. **Descarga de Plantilla Oficial (`GET /api/v1/patients/template/excel`):**
   - Genera una plantilla `.xlsx` lista para rellenar con un registro de ejemplo.

---

## 🚀 Requisitos e Instalación

### 1. Requisitos Previos
- **Python 3.10 o superior**
- **Microsoft ODBC Driver 17 o 18 for SQL Server**

### 2. Crear entorno virtual e instalar librerías

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Instalar dependencias (FastAPI, SQLAlchemy, PyODBC, Pandas, OpenPyXL, etc.)
pip install -r requirements.txt
```

### 3. Configurar `.env`

```env
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_SERVER=localhost
DB_PORT=1433
DB_NAME=PediatriaDB
DB_USER=sa
DB_PASSWORD=TuPasswordSeguro123!
DB_TRUST_SERVER_CERTIFICATE=yes

API_HOST=127.0.0.1
API_PORT=8000
API_DEBUG=True
```

---

## ▶️ Ejecución y Documentación Interactiva

Inicia el servidor con recarga en vivo:

```bash
uvicorn main:app --reload
```

Accede a Swagger UI en el navegador: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

### Endpoints Disponibles:

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/` | Health check del servicio |
| `GET` | `/api/v1/patients/template/excel` | Descarga la plantilla oficial en Excel |
| `GET` | `/api/v1/patients/export/excel` | Exporta todos los pacientes a un archivo `.xlsx` |
| `POST` | `/api/v1/patients/import/excel` | Sube un archivo Excel para registrar pacientes masivamente |
| `POST` | `/api/v1/patients` | Registra un paciente individual |
| `GET` | `/api/v1/patients/{patient_id}` | Consulta un paciente por ID |
| `GET` | `/api/v1/patients` | Lista pacientes con paginación (`skip`, `limit`) |
