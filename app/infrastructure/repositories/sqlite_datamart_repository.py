import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from app.domain.entities.variables_ppr import VariablesPPR
from app.domain.repositories.datamart_repository import DataMartRepositoryInterface
from app.infrastructure.models.datamart_models import (
    ArchivoCargadoModel,
    PersonalSaludModel,
    CitaHISModel,
    ItemDiagnosticoModel,
)

logger = logging.getLogger(__name__)


class SqliteDataMartRepository(DataMartRepositoryInterface):
    """
    Implementación del Data Mart en SQLite usando SQLAlchemy.
    Optimizado para inserciones por lotes e idempotencia (on conflict do nothing / update).
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def guardar_trama(
        self,
        nombre_archivo: str,
        tipo_formato: str,
        variables: List[VariablesPPR],
        usuario: str = "estadistica",
    ) -> Dict[str, Any]:
        """
        Inserta la trama en las tablas normalizadas del Data Mart:
        1. Registra archivo en `archivos_cargados`.
        2. Inserta atenciones únicas en `citas_his` (incluyendo `id_personal`).
        3. Inserta diagnósticos/procedimientos en `items_diagnostico`.
        """
        if not variables:
            return {
                "archivo_id": None,
                "total_registros_trama": 0,
                "citas_procesadas": 0,
                "items_procesados": 0,
                "meses_detectados": [],
            }

        # 1. Detectar meses únicos presentes en el lote de variables
        meses_detectados = sorted(
            list(
                {
                    v.Fecha_Atencion.strftime("%Y-%m")
                    for v in variables
                    if v.Fecha_Atencion
                }
            )
        )
        meses_str = ", ".join(meses_detectados)

        # 2. Registrar auditoría de carga
        archivo = ArchivoCargadoModel(
            nombre_archivo=nombre_archivo,
            tipo_formato=tipo_formato,
            fecha_carga=datetime.utcnow(),
            total_filas=len(variables),
            meses_detectados=meses_str,
            usuario_responsable=usuario,
            estado="CONSOLIDADO",
        )
        self.db.add(archivo)
        self.db.flush()  # Obtiene el ID autoincremental de la auditoría

        # 3. Preparar citas únicas para inserción
        citas_dict: Dict[str, Dict[str, Any]] = {}
        for v in variables:
            if v.Id_cita and v.Id_cita not in citas_dict:
                mes_periodo = (
                    v.Fecha_Atencion.strftime("%Y-%m")
                    if v.Fecha_Atencion
                    else "SIN_FECHA"
                )
                citas_dict[v.Id_cita] = {
                    "id_cita": v.Id_cita,
                    "id_archivo": archivo.id,
                    "id_personal": (v.Id_Personal.strip() if v.Id_Personal else None),
                    "fecha_atencion": v.Fecha_Atencion,
                    "mes_periodo": mes_periodo,
                    "lote": v.Lote or "",
                    "id_ups": v.Id_ups or "",
                    "edad": v.Edad if v.Edad is not None else 0,
                    "tipo_edad": (v.Tipo_Edad or "A").strip().upper(),
                }

        # 4. Preparar items únicos para inserción (evitando duplicar en el mismo lote)
        items_list: List[Dict[str, Any]] = []
        items_vistos = set()
        for v in variables:
            if not v.Id_cita or not v.Codigo_Item:
                continue
            key = (v.Id_cita, v.Codigo_Item.strip().upper(), v.Id_Correlativo)
            if key not in items_vistos:
                items_vistos.add(key)
                items_list.append(
                    {
                        "id_cita": v.Id_cita,
                        "codigo_item": v.Codigo_Item.strip().upper(),
                        "tipo_diagnostico": (v.Tipo_Diagnostico or "D").strip().upper(),
                        "valor_lab": v.Valor_Lab.strip() if v.Valor_Lab else None,
                        "id_correlativo": v.Id_Correlativo,
                        "id_correlativo_lab": v.Id_Correlativo_Lab,
                    }
                )

        BATCH_SIZE = 1000

        # Inserción de citas con ON CONFLICT DO NOTHING
        citas_to_insert = list(citas_dict.values())
        for i in range(0, len(citas_to_insert), BATCH_SIZE):
            batch_citas = citas_to_insert[i : i + BATCH_SIZE]
            stmt_citas = sqlite_insert(CitaHISModel).values(batch_citas)
            stmt_citas = stmt_citas.on_conflict_do_nothing(
                index_elements=["id_cita"]
            )
            self.db.execute(stmt_citas)

        # Inserción de items con ON CONFLICT DO NOTHING
        for i in range(0, len(items_list), BATCH_SIZE):
            batch_items = items_list[i : i + BATCH_SIZE]
            stmt_items = sqlite_insert(ItemDiagnosticoModel).values(batch_items)
            stmt_items = stmt_items.on_conflict_do_nothing(
                index_elements=["id_cita", "codigo_item", "id_correlativo"]
            )
            self.db.execute(stmt_items)

        self.db.commit()

        logger.info(
            f"Trama guardada exitosamente: Archivo {nombre_archivo} | "
            f"{len(citas_to_insert)} citas | {len(items_list)} items | Meses: {meses_str}"
        )

        return {
            "archivo_id": archivo.id,
            "total_registros_trama": len(variables),
            "citas_procesadas": len(citas_to_insert),
            "items_procesados": len(items_list),
            "meses_detectados": meses_detectados,
        }

    def obtener_variables_acumuladas(
        self,
        meses: Optional[List[str]] = None,
        anio: Optional[int] = None,
    ) -> List[VariablesPPR]:
        """
        Recupera las variables clínicas acumuladas realizando JOIN entre Citas e Items.
        """
        query = (
            self.db.query(
                CitaHISModel.id_cita,
                CitaHISModel.fecha_atencion,
                CitaHISModel.lote,
                CitaHISModel.id_ups,
                CitaHISModel.edad,
                CitaHISModel.tipo_edad,
                CitaHISModel.id_personal,
                ItemDiagnosticoModel.codigo_item,
                ItemDiagnosticoModel.tipo_diagnostico,
                ItemDiagnosticoModel.valor_lab,
                ItemDiagnosticoModel.id_correlativo,
                ItemDiagnosticoModel.id_correlativo_lab,
            )
            .join(ItemDiagnosticoModel, CitaHISModel.id_cita == ItemDiagnosticoModel.id_cita)
        )

        if meses:
            query = query.filter(CitaHISModel.mes_periodo.in_(meses))
        elif anio:
            query = query.filter(CitaHISModel.mes_periodo.like(f"{anio}-%"))

        query = query.order_by(
            CitaHISModel.fecha_atencion.asc(),
            CitaHISModel.id_cita.asc(),
            ItemDiagnosticoModel.id_correlativo.asc(),
        )

        rows = query.all()

        return [
            VariablesPPR(
                Id_cita=row.id_cita,
                Fecha_Atencion=row.fecha_atencion,
                Lote=row.lote or "",
                Id_ups=row.id_ups,
                Edad=row.edad,
                Tipo_Edad=row.tipo_edad,
                Codigo_Item=row.codigo_item,
                Tipo_Diagnostico=row.tipo_diagnostico,
                Valor_Lab=row.valor_lab,
                Id_Correlativo=row.id_correlativo,
                Id_Correlativo_Lab=row.id_correlativo_lab,
                Id_Personal=row.id_personal,
            )
            for row in rows
        ]

    def guardar_personal_maestro(
        self,
        personal_list: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Inserta o actualiza el catálogo maestro de personal de salud (Médicos, Enfermeras, etc.).
        Utiliza ON CONFLICT DO UPDATE sobre id_personal para actualizar nombres, dni y profesion.
        """
        if not personal_list:
            return {"total_recibidos": 0, "total_procesados": 0}

        BATCH_SIZE = 1000
        total_procesados = 0

        for i in range(0, len(personal_list), BATCH_SIZE):
            batch = personal_list[i : i + BATCH_SIZE]
            stmt = sqlite_insert(PersonalSaludModel).values(batch)
            stmt = stmt.on_conflict_do_update(
                index_elements=["id_personal"],
                set_={
                    "cod_profesion": stmt.excluded.cod_profesion,
                    "nombres": stmt.excluded.nombres,
                    "dni": stmt.excluded.dni,
                },
            )
            self.db.execute(stmt)
            total_procesados += len(batch)

        self.db.commit()
        logger.info(f"Maestro de personal actualizado: {total_procesados} registros procesados.")
        return {
            "total_recibidos": len(personal_list),
            "total_procesados": total_procesados,
        }

    def listar_personal(
        self,
        cod_profesion: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retorna la lista del personal de salud, opcionalmente filtrado por código de profesión.
        """
        query = self.db.query(PersonalSaludModel)
        if cod_profesion:
            query = query.filter(PersonalSaludModel.cod_profesion == cod_profesion.strip())
        query = query.order_by(PersonalSaludModel.nombres.asc())
        rows = query.all()
        return [
            {
                "id": r.id,
                "id_personal": r.id_personal,
                "cod_profesion": r.cod_profesion,
                "nombres": r.nombres,
                "dni": r.dni,
                "fecha_registro": r.fecha_registro.strftime("%Y-%m-%d %H:%M:%S") if r.fecha_registro else None,
            }
            for r in rows
        ]

    def listar_meses_disponibles(self) -> List[str]:
        """
        Retorna la lista ordenada cronológicamente de los meses presentes en el Data Mart.
        """
        results = (
            self.db.query(CitaHISModel.mes_periodo)
            .distinct()
            .order_by(CitaHISModel.mes_periodo.asc())
            .all()
        )
        return [r[0] for r in results if r[0] and r[0] != "SIN_FECHA"]

    def listar_archivos_cargados(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retorna el listado de archivos cargados en el Data Mart con su información de auditoría.
        """
        archivos = (
            self.db.query(ArchivoCargadoModel)
            .order_by(ArchivoCargadoModel.fecha_carga.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": a.id,
                "nombre_archivo": a.nombre_archivo,
                "tipo_formato": a.tipo_formato,
                "fecha_carga": a.fecha_carga.strftime("%Y-%m-%d %H:%M:%S") if a.fecha_carga else None,
                "total_filas": a.total_filas,
                "meses_detectados": a.meses_detectados,
                "usuario_responsable": a.usuario_responsable,
                "estado": a.estado,
            }
            for a in archivos
        ]

    def reiniciar_datamart(self) -> bool:
        """
        Elimina todas las filas de items, citas, personal y archivos cargados.
        """
        try:
            self.db.query(ItemDiagnosticoModel).delete()
            self.db.query(CitaHISModel).delete()
            self.db.query(PersonalSaludModel).delete()
            self.db.query(ArchivoCargadoModel).delete()
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error al reiniciar Data Mart: {e}")
            raise e
