from skyfield.api import load, Topos
from datetime import datetime

# Carregar dados TLE para o satélite Landsat 8 (TLE pode ser obtido de serviços como Celestrak)
def get_satellite_position():
    stations_url = 'https://www.n2yo.com/satellite/?s=39084'
    satellites = load.tle_file(stations_url)
    by_name = {sat.name: sat for sat in satellites}
    
    landsat = by_name['LANDSAT 8']
    
    # Definir o momento atual para calcular a posição do satélite
    ts = load.timescale()
    t = ts.now()
    
    # Definir um local para visualizar a passagem do satélite
    location = Topos(latitude_degrees=41.0, longitude_degrees=-74.0)
    
    # Calcular a posição do satélite
    geocentric = landsat.at(t)
    subpoint = geocentric.subpoint()

    return subpoint.latitude.degrees, subpoint.longitude.degrees

latitude, longitude = get_satellite_position()
print(f"Landsat 8 está atualmente em {latitude}° de latitude e {longitude}° de longitude.")
