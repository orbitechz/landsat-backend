from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import ee
from starlette.responses import JSONResponse

from api.classes.SentinelClient import SentinelClient


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
    landsat_collection = ee.ImageCollection("") \
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

@earthengineRouter.get("/gee-data2")
async def get_gee_data():
    # Exemplo de filtro Landsat
    collection = ee.ImageCollection('LANDSAT/LC09/C02/T1_TOA')\
        .filterDate('2012-01-01', '2024-12-31')\
        .filterBounds(ee.Geometry.Point([-54.570679921692374, -25.55270154839337 ]))

    # Pegando as informações de metadados como exemplo
    info = collection.getInfo()
    return info
  
@earthengineRouter.get("/gee-data")
async def get_gee_urls():
    try:
        # Coleção de imagens do Landsat 9
        collection = ee.ImageCollection('LANDSAT/LC09/C02/T2')

        # Selecionar a imagem mais recente da coleção
        image = collection.filterDate('2023-01-01', '2023-02-01').mosaic()


        # Parâmetros de visualização para as bandas RGB
        vis_params = {
            'bands': ['B2', 'B3', 'B4'],  
            'min': 100,
            'max': 3500,
            'gamma': 1.4
        }

        # Gerar um ID de mapa e URL para tiles (Google Earth Engine)
        map_id_dict = image.getMapId(vis_params)
        tile_url = map_id_dict['tile_fetcher'].url_format

        # Retornar a URL dos tiles para o frontend
        return JSONResponse({"tile_url": tile_url})
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)