from fastapi import FastAPI, HTTPException, APIRouter
import requests
from skyfield.api import load, EarthSatellite
from typing import List, Dict


geolocationRealtime = APIRouter()

API_KEY = '9PG6XR-NBWE6Z-68AWZD-5CJL'  # Substitua pela sua chave de API do N2YO

# Função para buscar o TLE a partir da API do N2YO
def fetch_tle(satellite_id: str) -> List[str]:
    # Corrigir a URL para ter o '?' antes do apiKey
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{satellite_id}?apiKey={API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching TLE data from N2YO.")
    
    data = response.json()
    
    # Corrigir a extração do TLE e dividir corretamente em duas linhas
    tle = data.get('tle', None)
    
    if not tle:
        raise HTTPException(status_code=404, detail="TLE data not found for the given satellite ID.")
    
    # Separar o TLE em duas linhas usando '\r\n'
    tle_lines = tle.split("\r\n")
    
    if len(tle_lines) != 2:
        raise HTTPException(status_code=500, detail="Invalid TLE data format.")
    
    return tle_lines

# Função para calcular o bounding box com base no TLE e na posição atual
def get_satellite_bbox(tle_lines: List[str]) -> Dict[str, Dict[str, float]]:
    try:
        # Verificar se as duas linhas do TLE estão corretas e passar separadamente
        line1 = tle_lines[0]
        line2 = tle_lines[1]

        # Carregar o satélite usando os dados TLE
        satellite = EarthSatellite(line1, line2, 'satellite', load.timescale())
        ts = load.timescale()
        current_time = ts.now()
        geocentric = satellite.at(current_time)

        # Extrair latitude e longitude da subponto (ponto na Terra diretamente abaixo do satélite)
        longitude = geocentric.subpoint().longitude.degrees
        latitude = geocentric.subpoint().latitude.degrees

        # Definir delta para o bounding box
        delta = 0.5
        bbox = {
            "min_latitude": latitude - delta,
            "max_latitude": latitude + delta,
            "min_longitude": longitude - delta,
            "max_longitude": longitude + delta,
        }

        return {"bbox": bbox}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))