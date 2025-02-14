from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Boolean
from ..ddbb_connection import RepComunBase

class Centro(RepComunBase):

    __tablename__ = "Centros"

    Id = mapped_column(Integer, primary_key=True)
    Nombre = mapped_column(String, nullable=False)
    IdEmpresa = mapped_column(Integer, nullable=False)
    IdTipoCentro = mapped_column(Integer, nullable=False)
    IdZonaHoraria = mapped_column(Integer, nullable=True)
    Rega = mapped_column(String, nullable=True)
    Activo = mapped_column(Boolean, nullable=False)