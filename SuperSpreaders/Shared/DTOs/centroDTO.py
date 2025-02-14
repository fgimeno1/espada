from __future__ import annotations
from RepComun.DataLayer.Enitites import Localizacion, Centro
from dataclasses import dataclass

@dataclass
class CentroDTO:

    Id : int
    Nombre : str
    Activo : bool
    CodPostal : int | None = None
    Latitud : float | None = None
    Longitud : float | None = None

    @staticmethod
    def mapCentroToDTO(values : Centro | list[Centro]) -> "CentroDTO" | list["CentroDTO"]:

        if isinstance(values, list):
            return list(map(lambda x : CentroDTO(Id = x.Id,
                                                 Nombre = x.Nombre,
                                                 Activo = x.Activo),
                            values))

        elif isinstance(values, Centro):

            return CentroDTO(Id = values.Id,
                             Nombre = values.Nombre,
                             Activo = values.Activo)

        else:

            raise Exception("Not Centro or list of Centros")

    @staticmethod
    def mapCentroLocToDTO(values : tuple[Centro, Localizacion] | list[tuple[Centro, Localizacion]]) -> "CentroDTO" | list["CentroDTO"]:

        if isinstance(values, list[tuple[Centro, Localizacion]]):
            return list(map(lambda x : CentroDTO(Id = x[0].Id,
                                                 Nombre = x[0].Nombre,
                                                 Activo = x[0].Activo,
                                                 CodPostal = x[1].CodPostal,
                                                 Latitud = x[1].Latitud,
                                                 Longitud = x[1].Longitud),
                            values))

        elif isinstance(values, tuple[Centro, Localizacion]):

            return CentroDTO(Id = values[0].Id,
                             Nombre = values[0].Nombre,
                             Activo = values[0].Activo,
                             Latitud = values[1].Latitud,
                             Longitud = values[1].Longitud,
                             CodPostal = values[1].CodPostal)

        else:

            raise Exception("Not tuple[Centro, Localizacion] or list of tuple[Centros, Localizacion]")
