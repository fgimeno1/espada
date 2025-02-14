from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from ..ddbb_connection import ExternalBase

class TipoRegistroVisita(ExternalBase):

    __tablename__ = "TipoRegistroVisita"

    Id = mapped_column(Integer, primary_key=True)
    Nombre = mapped_column(String, nullable=False)