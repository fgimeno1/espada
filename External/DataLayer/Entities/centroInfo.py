from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, DateTime, Boolean, ForeignKey
from ..ddbb_connection import ExternalBase

class CentroInfo(ExternalBase):

    __tablename__ = "CentroInfo"

    Id = mapped_column(Integer, primary_key=True)
    IdTipoGranja = mapped_column(Integer, nullable=True)
    IdEstadoSanitario = mapped_column(Integer, nullable=True)
    IdTipoSubclasificacion = mapped_column(Integer, ForeignKey("TipoSubClasificacion.Id"), nullable=True)
    UltimaEntradaAnimales = mapped_column(DateTime, nullable=True)
    PlazasCerdas = mapped_column(Integer, nullable=True)
    PlazasLechones = mapped_column(Integer, nullable=True)
    PlazasCerdos = mapped_column(Integer, nullable=True)
    IdGrupo = mapped_column(Integer, nullable=True)
    MetrosGenerarVisita = mapped_column(Integer, nullable=True)
    Activo = mapped_column(Boolean, nullable=False)