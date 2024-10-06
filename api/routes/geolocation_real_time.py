from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime
from api.classes.SatelliteDataRequest import SatelliteDataRequest
from skyfield.api import load

from api.services.getrealtime import fetch_tle
from api.services.getrealtime import get_predicted_bbox

geolocationRealtime = APIRouter()

# Função simulada para buscar dados do Landsat
def get_landsat_data(token: str, bounds: List[float], from_date: datetime, to_date: datetime) -> Dict:
    # Lógica para buscar dados do Landsat (simulado aqui)
    return {
        "status": "success",
        "data": {
            "bounds": bounds,
            "from_date": from_date,
            "to_date": to_date,
            "images": []  # Exemplo: lista de URLs de imagens
        }
    }

# Função para obter o bounding box da posição do satélite
def get_satellite_bbox(tle: str) -> Dict[str, Dict[str, float]]:
    satellite = load.tle_file([tle])[0]  # Carregando o TLE
    ts = load.timescale()
    current_time = ts.now()
    geocentric = satellite.at(current_time)

    # Convertendo a posição do satélite de AU para graus
    longitude = geocentric.position.au[0] * 180 / 3.141592653589793
    latitude = geocentric.position.au[1] * 180 / 3.141592653589793

    # Definindo o tamanho do bounding box (pode ser ajustado conforme necessário)
    delta = 0.5  # Em graus

    # Calculando o bounding box
    bbox = {
        "min_latitude": latitude - delta,
        "max_latitude": latitude + delta,
        "min_longitude": longitude - delta,
        "max_longitude": longitude + delta,
    }

    return {"bbox": bbox}

# Endpoint para capturar imagens de satélite
@geolocationRealtime.post("/geolocation/satellite-data")
async def satellite_data(request: SatelliteDataRequest):
    try:
        image_data = get_landsat_data(request.token, request.bounds, request.from_date, request.to_date)
        return {"status": "success", "message": "Satellite data fetched successfully!", "data": image_data}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para calcular a rota do satélite (agora retorna o bbox)
@geolocationRealtime.post("/geolocation/satellite-route")
async def satellite_route(tle: List[str]):
    try:
        bbox = get_satellite_bbox(tle)
        return {"status": "success", "bbox": bbox}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint para buscar o TLE e calcular o bounding box
@geolocationRealtime.get("/geolocation/tle/{satellite_id}")
async def predict_satellite_bbox(satellite_id: str):
    try:
        # Buscar os dados TLE com base no satellite_id
        tle = fetch_tle(satellite_id)

        # Log para verificar o formato do TLE
        print(f"TLE recebido: {tle}")
        
        # Calcular o bounding box previsto com base nos dados TLE
        predicted_bbox = get_predicted_bbox(tle)
        
        return {
            "status": "success",
            "tle": tle,  # Retorna as linhas TLE
            "predicted_bbox": predicted_bbox  # Retorna o bounding box previsto
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
