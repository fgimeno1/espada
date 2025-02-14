from ..ddbb_connection import SESSIONMAKER
from ..Enitites import Localizacion

async def asyncGetAllLocalizacion() -> list[Localizacion]:

    ret = None

    with SESSIONMAKER() as session:
        ret = session.query(Localizacion).all()

    return ret