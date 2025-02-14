from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from ..ddbb_connection import ExternalBase

class EstadoSanitario(ExternalBase):

    __tablename__ = "EstadoSanitario"

    Id = mapped_column(Integer, primary_key=True)
    Codigo = mapped_column(String, nullable=False)
    Nombre = mapped_column(String, nullable=False)
    IdEspecie = mapped_column(Integer, nullable=True)
    Orden = mapped_column(Integer, nullable=False)