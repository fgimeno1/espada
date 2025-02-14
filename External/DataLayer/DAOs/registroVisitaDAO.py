from ..Entities import RegistroVisita, CentroInfo
from ..ddbb_connection import SESSIONMAKER
from sqlalchemy import between
from datetime import datetime


async def asyncGetAllRegistroVisita() -> list[RegistroVisita]:

    ret = None

    with SESSIONMAKER() as session:
        ret = session.query(RegistroVisita).all()

    return ret

async def asyncGetAllVehicleRegistroVisita() -> list[RegistroVisita]:

    ret = None

    with SESSIONMAKER() as session:
        ret = session.query(RegistroVisita).where(RegistroVisita.IdVehiculo is not None).all()

    return ret

async def asyncGetAllVehicleRegistroVisitaInfo() -> list[tuple[RegistroVisita, CentroInfo]]:

    ret = None

    with SESSIONMAKER() as session:
        ret = session.query(RegistroVisita, CentroInfo).join(CentroInfo, RegistroVisita.IdCentro == CentroInfo.Id).all()

    return ret

async def asyncGetAllVehicleRegistroVisitaInfoByPeriod(start : datetime, end : datetime) -> list[tuple[RegistroVisita, CentroInfo]]:


    ret = None

    with SESSIONMAKER() as session:
        ret = session.query(RegistroVisita, CentroInfo
                            ).join(CentroInfo, RegistroVisita.IdCentro == CentroInfo.Id
                                   ).where(between(RegistroVisita.Fecha, start, end)
                                           ).all()

    return ret

async def asyncGetAllVehicleRegistroVisitaInfoByParameters(idCentro : int | None = None,
                                                           isActivo : bool | None = True,
                                                           fechaComienzo : datetime | None = None,
                                                           fechaFin : datetime | None = None) -> list[tuple[RegistroVisita, CentroInfo]]:
    
    ret = None

    with SESSIONMAKER() as session:

        myQuery = session.query(
                RegistroVisita, CentroInfo
            ).join(
                CentroInfo, RegistroVisita.IdCentro == CentroInfo.Id
            ).where(RegistroVisita.IdVehiculo is not None)

        if idCentro is not None:
            myQuery = myQuery.where(RegistroVisita.IdCentro == idCentro)

        if isActivo:
            myQuery = myQuery.where(CentroInfo.Activo)

        if fechaComienzo is not None:
            myQuery = myQuery.where(RegistroVisita.Fecha >= fechaComienzo)

        if fechaFin is not None:
            myQuery = myQuery.where(RegistroVisita.Fecha <= fechaFin)

        ret = myQuery.all()

    return ret