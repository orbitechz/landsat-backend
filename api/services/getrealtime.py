from fastapi import FastAPI, HTTPException, APIRouter
import requests
from skyfield.api import load, EarthSatellite
from datetime import timedelta


geolocationRealtime = APIRouter()

API_KEY = '9PG6XR-NBWE6Z-68AWZD-5CJL'  # Substitua pela sua chave de API do N2YO

# Função para buscar o TLE a partir da API do N2YO
def fetch_tle(satellite_id: str) -> dict:
    # Corrigir a URL para incluir o '?' antes de apiKey
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{satellite_id}?apiKey={API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching TLE data from N2YO.")
    
    data = response.json()
    
    tle = data.get('tle', None)
    
    if not tle:
        raise HTTPException(status_code=404, detail="TLE data not found for the given satellite ID.")
    
    return {
        "line1": tle.split("\r\n")[0],  # Pegar a primeira linha do TLE
        "line2": tle.split("\r\n")[1],  # Pegar a segunda linha do TLE
    }

# Função para calcular o bounding box com base no TLE e na posição prevista do satélite
def get_predicted_bbox(tle: dict) -> dict:
    try:
        # Carregar o satélite usando os dados TLE
        line1 = tle['line1']
        line2 = tle['line2']
        
        satellite = EarthSatellite(line1, line2, 'satellite', load.timescale())
        ts = load.timescale()
        
        # Calcular a posição do satélite 10 minutos a partir do momento atual
        current_time = ts.now()
        future_time = current_time + timedelta(minutes=10)  # Pode ajustar o tempo conforme necessário
        
        geocentric = satellite.at(future_time)

        # Extrair latitude e longitude da subponto (ponto na Terra diretamente abaixo do satélite)
        longitude = geocentric.subpoint().longitude.degrees
        latitude = geocentric.subpoint().latitude.degrees

        # Definir delta para o bounding box
        delta = 0.5  # Pode ajustar o delta conforme necessário
        bbox = {
            "min_latitude": latitude - delta,
            "max_latitude": latitude + delta,
            "min_longitude": longitude - delta,
            "max_longitude": longitude + delta,
        }

        return bbox
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating predicted bounding box: {str(e)}")
