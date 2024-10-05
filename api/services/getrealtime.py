from fastapi import FastAPI, HTTPException
import requests
from skyfield.api import load

app = FastAPI()

API_KEY = '9PG6XR-NBWE6Z-68AWZD-5CJL'  # Substitua pela sua chave de API do N2YO

# Função para buscar o TLE a partir da API do N2YO
def fetch_tle(satellite_id: str):
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{satellite_id}&apiKey={API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching TLE data from N2YO.")
    
    data = response.json()
    
    if 'tle' not in data or not data['tle']:
        raise HTTPException(status_code=404, detail="TLE data not found for the given satellite ID.")
    
    return data['tle']  # Retorna a linha do TLE

# Função para calcular o bounding box com base no TLE e na posição atual
@app.get("/geolocation/tle/{satellite_id}")
async def get_satellite_bbox(satellite_id: str):
    try:
        # Obtenção do TLE via API N2YO
        tle_data = fetch_tle(satellite_id)
        
        # O TLE contém duas linhas separadas, então dividimos as strings
        tle_lines = tle_data.splitlines()

        # Carregar o TLE no Skyfield
        satellite = load.tle_file(tle_lines)[0]  # Carrega o TLE no formato esperado pelo Skyfield
        
        # Carregar o tempo atual
        ts = load.timescale()
        current_time = ts.now()

        # Obter a posição geocêntrica do satélite
        geocentric = satellite.at(current_time)
        
        # Posição geocêntrica do satélite (latitude e longitude)
        subpoint = geocentric.subpoint()
        latitude = subpoint.latitude.degrees
        longitude = subpoint.longitude.degrees

        # Definir o tamanho do bounding box (ajustável)
        delta = 0.5  # Em graus, por exemplo

        # Calcular o bounding box
        bbox = {
            "min_latitude": latitude - delta,
            "max_latitude": latitude + delta,
            "min_longitude": longitude - delta,
            "max_longitude": longitude + delta,
        }

        return {"bbox": bbox}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
