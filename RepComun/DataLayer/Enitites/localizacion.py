from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey
from ..ddbb_connection import RepComunBase

class Localizacion(RepComunBase):

    __tablename__ = "Localizacion"

    Id = mapped_column(Integer, primary_key=True)
    IdCentro = mapped_column(Integer, ForeignKey("Centro.Id"))
    Direccion = mapped_column(String, nullable=True)
    Localidad = mapped_column(String, nullable=True)
    CodPostal = mapped_column(Integer, nullable=True)
    IdPais = mapped_column(Integer, nullable=False)
    IdTipoLocalizacion = mapped_column(Integer, nullable=True)
    Latitud = mapped_column(Float, nullable=True)
    Longitud = mapped_column(Float, nullable=True)