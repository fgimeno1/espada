from ..ddbb_connection import SESSIONMAKER
from ..Enitites import Localizacion, Centro

async def asyncGetAllCentro() -> list[Centro]:

    ret = None

    with SESSIONMAKER() as session:
        ret = session.query(Centro).all()

    return ret

async def asyncGetAllCentroLoc() -> list[tuple[Centro, Localizacion]]:

    ret = None

    with SESSIONMAKER() as session:
        ret = session.query(Centro, Localizacion).join(Centro.Id == Localizacion.IdCentro).all()

    return ret

async def asyncGetCentroByEmpresa(empresa : int) -> list[Centro]:

    ret = None

    with SESSIONMAKER() as session:
        ret = session.query(Centro).where(Centro.IdEmpresa == empresa).all()

    return ret