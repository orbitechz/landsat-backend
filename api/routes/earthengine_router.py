from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import ee
import geemap 

# Inicializando a
# API do Earth Engine
ee.Authenticate()
ee.Initialize(project='landsat-437722')



earthengineRouter = APIRouter()

@earthengineRouter.get("/landsat-data")
async def get_landsat_data(request: Request):
    # Parâmetros de entrada da requisição (coordenadas e data)
    lat = 6.746
    lon = 6
    start_date = '2017-01-01'
    end_date = '2017-12-31'

    # Definindo a região de interesse
    point = ee.Geometry.Point([lon, lat])
    
    # Criando um buffer de 500 metros em torno do ponto
    region = point.buffer(500)

    # Coleção Landsat 8 Surface Reflectance
    landsat_collection = ee.ImageCollection("LANDSAT/LC08/C02/T1_RT_TOA") \
        .filterBounds(region) \
        .filterDate(start_date, end_date) \
        .limit(10)  # Limitando para 5 imagens

    # Pegando as URLs de visualização das imagens
    def get_image_url(image):
        # Seleciona as bandas RGB para visualização
        rgb_image = image.select(['B4', 'B3', 'B2'])  # Red, Green, Blue
        
        # Define os parâmetros de visualização
        visualization_params = {
            'region': region,  # Usando a região do buffer
            'scale': 30,
            'min': 100,   # Valor mínimo para a escala de cores
            'max': 3000  # Valor máximo para a escala de cores
        }

        return rgb_image.getThumbURL(visualization_params)

    image_list = landsat_collection.toList(5)  # Pegando as primeiras 5 imagens
    urls = [get_image_url(ee.Image(image_list.get(i))) for i in range(5)]

    # Retornando os URLs das imagens
    return JSONResponse(content=urls)
