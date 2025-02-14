from dataclasses import dataclass
from datetime import datetime

@dataclass
class MovementDTO:

    BeginCenterId : int
    EndCenterId : int
    BeginCenterSubclasificationId : int
    EndCenterSubclasificationId : int
    StartDatetime : datetime
    EndDatetime : datetime
    VehicleId : int
