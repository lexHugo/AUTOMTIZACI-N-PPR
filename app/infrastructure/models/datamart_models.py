from datetime import datetime, date
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from app.infrastructure.database.session import Base


class ArchivoCargadoModel(Base):
    """
    Tabla de Auditoría y Trazabilidad de Cargas.
    Registra cada archivo Excel o CSV procesado en el Data Mart.
    """
    __tablename__ = "archivos_cargados"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre_archivo = Column(String(255), nullable=False)
    tipo_formato = Column(String(50), default="EXCEL", nullable=False)  # "EXCEL" o "CSV"
    fecha_carga = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_filas = Column(Integer, default=0, nullable=False)
    meses_detectados = Column(String(255), nullable=True)  # Ej: "2026-01, 2026-02"
    usuario_responsable = Column(String(100), default="estadistica", nullable=False)
    estado = Column(String(50), default="CONSOLIDADO", nullable=False)  # "CONSOLIDADO", "EN_REVISION", "CERRADO"

    # Relación con las citas contenidas en este archivo
    citas = relationship("CitaHISModel", back_populates="archivo", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ArchivoCargado(id={self.id}, nombre='{self.nombre_archivo}', meses='{self.meses_detectados}')>"


class PersonalSaludModel(Base):
    """
    Tabla Maestra de Personal de Salud (Médicos, Enfermeras, etc.).
    Permite validar la profesión del profesional que atendió la cita para
    cálculos donde se exige estrictamente atención por Médico.
    """
    __tablename__ = "personal_salud"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_personal = Column(String(50), unique=True, index=True, nullable=False)
    cod_profesion = Column(String(20), index=True, nullable=False)  # Ej: "01" (Médico), "02" (Enfermera)
    nombres = Column(String(255), nullable=True)
    dni = Column(String(20), index=True, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relación con las citas atendidas por este profesional
    citas = relationship("CitaHISModel", back_populates="personal")

    def __repr__(self):
        return f"<PersonalSalud(id_personal='{self.id_personal}', nombres='{self.nombres}', prof='{self.cod_profesion}')>"


class CitaHISModel(Base):
    """
    Tabla de Atenciones / Citas Médicas del HIS MINSA.
    Contiene la cabecera del encuentro (paciente, fecha, edad, servicio/UPS y personal).
    """
    __tablename__ = "citas_his"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_cita = Column(String(100), unique=True, index=True, nullable=False)
    id_archivo = Column(Integer, ForeignKey("archivos_cargados.id"), index=True, nullable=True)
    id_personal = Column(String(50), ForeignKey("personal_salud.id_personal"), index=True, nullable=True)
    fecha_atencion = Column(Date, index=True, nullable=False)
    mes_periodo = Column(String(7), index=True, nullable=False)  # Formato: "YYYY-MM" (ej: "2026-01")
    lote = Column(String(50), nullable=True)
    id_ups = Column(String(50), index=True, nullable=False)  # Ej: 303712 (Pediatría), 301204 (Inmunizaciones)
    edad = Column(Integer, default=0, nullable=False)
    tipo_edad = Column(String(10), default="A", nullable=False)  # "A" (Años), "M" (Meses), "D" (Días)

    # Relaciones
    archivo = relationship("ArchivoCargadoModel", back_populates="citas")
    personal = relationship("PersonalSaludModel", back_populates="citas")
    items = relationship("ItemDiagnosticoModel", back_populates="cita", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_citas_periodo_ups", "mes_periodo", "id_ups"),
    )

    def __repr__(self):
        return f"<CitaHIS(id_cita='{self.id_cita}', fecha='{self.fecha_atencion}', ups='{self.id_ups}', personal='{self.id_personal}')>"


class ItemDiagnosticoModel(Base):
    """
    Tabla de Diagnósticos y Procedimientos de la Cita.
    Contiene los códigos CIE-10 (Morbilidad) y CPT (Vacunas) registrados.
    """
    __tablename__ = "items_diagnostico"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_cita_ref = Column(Integer, ForeignKey("citas_his.id"), index=True, nullable=True)
    id_cita = Column(String(100), index=True, nullable=False)
    codigo_item = Column(String(50), index=True, nullable=False)  # Ej: "D509", "J00X", "90708"
    tipo_diagnostico = Column(String(10), default="D", nullable=False)  # "D" (Definitivo), "P" (Presuntivo), "R" (Repetido)
    valor_lab = Column(String(50), nullable=True)  # Ej: "1", "2", "3", "SF1"
    id_correlativo = Column(Integer, nullable=True)
    id_correlativo_lab = Column(Integer, nullable=True)

    # Relación
    cita = relationship("CitaHISModel", back_populates="items")

    __table_args__ = (
        # Regla única de integridad para evitar duplicar diagnósticos exactos en la misma cita
        UniqueConstraint("id_cita", "codigo_item", "id_correlativo", name="uq_cita_item_correlativo"),
        Index("ix_items_codigo_dx", "codigo_item", "tipo_diagnostico"),
    )

    def __repr__(self):
        return f"<ItemDiagnostico(id_cita='{self.id_cita}', item='{self.codigo_item}', dx='{self.tipo_diagnostico}')>"
