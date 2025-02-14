from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, DateTime, String, Boolean, ForeignKey
from ..ddbb_connection import ExternalBase

class RegistroVisita(ExternalBase):

    __tablename__ = "RegistroVisita"

    Id = mapped_column(Integer, primary_key=True)
    IdCentro = mapped_column(Integer, ForeignKey("CentroInfo.Id"), nullable=False)
    IdPersona = mapped_column(Integer)
    IdVehiculo = mapped_column(Integer)
    IdResultadoRegla = mapped_column(Integer)
    Fecha = mapped_column(DateTime)
    FechaContactoAnimales = mapped_column(DateTime)
    IdUsuarioAutorizador = mapped_column(Integer)
    Descripcion = mapped_column(String)
    IdEstadoSanitario = mapped_column(Integer)
    Automatica = mapped_column(Boolean)
    IndNueva = mapped_column(Boolean)

    #TODO: Definir relaciones