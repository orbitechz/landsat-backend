from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel


# Modelo para os dados da requisição do satélite
class SatelliteDataRequest(BaseModel):
    token: str
    bounds: List[float]  # Defina como uma lista de floats para coordenadas
    from_date: datetime
    to_date: datetime