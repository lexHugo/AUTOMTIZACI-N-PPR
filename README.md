# Pediatría PPR1001 - Arquitectura Limpia (Clean Architecture)

Sistema especializado para el procesamiento de tramas HIS MINSA, cálculo de las 9 actividades operativas e indicadores del programa presupuestal **PPR1001** y persistencia histórica en **SQL Server**.

---

## 🏛️ Estructura del Proyecto

```
PEDIATRIA_PPR/
│
├── app/
│   │
│   ├── domain/                         # CAPA DE DOMINIO (El núcleo puro)
│   │   ├── entities/
│   │   │   ├── variables_ppr.py        # Entidad VariablesPPR (datos del HIS filtrados)
│   │   │   └── historico_ppr.py        # Entidad HistoricoPPR (datos consolidados para BD)
│   │   ├── repositories/
│   │   │   └── historico_ppr_repository.py # Interfaz abstracta del repositorio histórico
│   │   └── exceptions/
│   │       └── domain_exceptions.py
│   │
│   ├── application/                    # CAPA DE APLICACIÓN
│   │   ├── dtos/
│   │   │   └── indicadores_dto.py      # IndicadorDTO con las 9 actividades operativas
│   │   ├── ports/
│   │   │   ├── ppr1001_interface.py    # Puerto con los métodos de cálculo de cada actividad
│   │   │   └── his_excel_reader_port.py # Puerto abstracto para la lectura del Excel HIS
│   │   └── use_cases/
│   │       └── procesar_ppr1001_use_case.py # CASO DE USO PRINCIPAL (Orquestador único)
│   │
│   ├── infrastructure/                 # CAPA DE INFRAESTRUCTURA
│   │   ├── config/settings.py          # Conexión SQL Server con pyodbc
│   │   ├── database/session.py         # SQLAlchemy Base y SessionLocal
│   │   ├── models/
│   │   │   └── historico_ppr_model.py  # Modelo ORM mapeado a SQL Server (historico_ppr1001)
│   │   ├── repositories/
│   │   │   └── sqlalchemy_historico_ppr_repository.py # Guardado y consulta histórica
│   │   └── services/
│   │       ├── pandas_his_excel_reader.py # Lector y filtro de columnas con Pandas
│   │       └── ppr1001.py              # SERVICIO DONDE SE INYECTAN LAS 9 FÓRMULAS
│   │
│   └── presentation/                   # CAPA DE PRESENTACIÓN (FastAPI)
│       ├── api/
│       │   ├── dependencies.py         # Inyección de dependencias
│       │   └── v1/
│       │       ├── router.py
│       │       └── endpoints/
│       │           └── ppr1001.py      # Endpoints HTTP (/procesar y /historico)
│       └── schemas/
│           └── indicadores_schema.py   # Esquemas Pydantic para el Frontend
│
├── main.py                             # Punto de entrada de FastAPI
├── requirements.txt                    # Dependencias
├── .env.example / .env                 # Configuración de SQL Server
└── README.md
```

---

## 🎯 ¿Dónde inyectar la lógica de cada actividad operativa?

Toda la lógica de las fórmulas reside en el archivo:
👉 [`app/infrastructure/services/ppr1001.py`](file:///C:/Users/hugo_/Desktop/PEDIATRIA_PPR/app/infrastructure/services/ppr1001.py)

Encontrarás un método dedicado para cada actividad:
- `calcular_3325401(variables: List[VariablesPPR]) -> str`
- `calcular_3325402(variables: List[VariablesPPR]) -> str`
- `calcular_3325403(variables: List[VariablesPPR]) -> str`
- `calcular_3325404(variables: List[VariablesPPR]) -> str`
- `calcular_3325405(variables: List[VariablesPPR]) -> str`
- `calcular_3325406(variables: List[VariablesPPR]) -> str`
- `calcular_3325407(variables: List[VariablesPPR]) -> str`
- `calcular_3325408(variables: List[VariablesPPR]) -> str`
- `calcular_3325508(variables: List[VariablesPPR]) -> str`

---

## 🌐 Endpoints Disponibles en FastAPI

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/v1/ppr1001/procesar` | Recibe el archivo `.xlsx` del HIS, calcula los 9 indicadores, guarda el registro histórico en SQL Server y retorna el JSON al frontend. |
| `GET` | `/api/v1/ppr1001/historico` | Retorna los procesamientos guardados en SQL Server para visualización histórica o auditoría. |
