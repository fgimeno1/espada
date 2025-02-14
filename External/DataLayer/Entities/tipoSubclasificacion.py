from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from ..ddbb_connection import ExternalBase

class TipoSubclasificacion(ExternalBase):

    __tablename__ = "TipoSubclasificacion"

    Id = mapped_column(Integer, primary_key=True)
    Nombre = mapped_column(String, nullable=False)