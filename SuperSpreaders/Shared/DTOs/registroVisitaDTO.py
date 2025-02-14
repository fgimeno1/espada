from dataclasses import dataclass
from datetime import datetime
from External.DataLayer.Entities import RegistroVisita, CentroInfo

@dataclass
class RegistroVisitaDTO:

    Id : int
    IdCentro : int
    Fecha : datetime
    IdPersona : int | None = None
    IdVehiculo : int | None = None
    IdTipoSubclasificacion : int | None = None

    @staticmethod
    def mapRegistroVisitaToDTO(values : RegistroVisita | list[RegistroVisita]) -> list["RegistroVisitaDTO"]:

        if isinstance(values, list):

            return list(
                map(
                    lambda x : RegistroVisitaDTO(
                        Id = x.Id,
                        IdCentro = x.IdCentro,
                        IdPersona = x.IdPersona,
                        IdVehiculo = x.IdVehiculo,
                        Fecha = x.Fecha
                    ), 
                    values)
            )

        elif isinstance(values, RegistroVisita):
            return RegistroVisitaDTO(
                Id = values.Id,
                IdCentro = values.IdCentro,
                IdPersona = values.IdPersona,
                IdVehiculo = values.IdVehiculo,
                Fecha = values.Fecha
            )

        else:
            raise Exception("The input is not a RegistroVisita or a list of RegistroVisita")
        
    @staticmethod
    def mapRegistroVisitaInfoToDTO(values : tuple[RegistroVisita, CentroInfo] | list[tuple[RegistroVisita, CentroInfo]]) -> list["RegistroVisitaDTO"]:
    
        if isinstance(values, list):
        
            return list(
                map(
                    lambda x : RegistroVisitaDTO(
                        Id = x[0].Id,
                        IdCentro = x[0].IdCentro,
                        IdPersona = x[0].IdPersona,
                        IdVehiculo = x[0].IdVehiculo,
                        Fecha = x[0].Fecha,
                        IdTipoSubclasificacion=x[1].IdTipoSubclasificacion
                    ), 
                    values)
            )

        elif isinstance(values, tuple):
            return RegistroVisitaDTO(
                Id = values[0].Id,
                IdCentro = values[0].IdCentro,
                IdPersona = values[0].IdPersona,
                IdVehiculo = values[0].IdVehiculo,
                Fecha = values[0].Fecha,
                IdTipoSubclasificacion=values[1].IdTipoSubclasificacion
            )

        else:
            raise Exception("The input is not a RegistroVisita or a list of RegistroVisita")
        
