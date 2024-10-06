from fastapi import APIRouter, Query, Request
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
        collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA')

        # Selecionar a imagem mais recente da coleção
        image = collection.filterDate('2017-01-01', '2017-01-16').mosaic()


        # Parâmetros de visualização para as bandas RGB
        vis_params = {
            'bands': ['B2', 'B3', 'B4'],  
            'min': 0,
            'max': 0.4,
            'gamma': 1.4
        }

        # Gerar um ID de mapa e URL para tiles (Google Earth Engine)
        map_id_dict = image.getMapId(vis_params)
        tile_url = map_id_dict['tile_fetcher'].url_format

        # Retornar a URL dos tiles para o frontend
        return JSONResponse({"tile_url": tile_url})
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@earthengineRouter.get("/gee-data-coords")
async def get_gee_urls_coords(
    lat_min: float = Query(..., description="Latitude mínima do retângulo de coordenadas"),
    lon_min: float = Query(..., description="Longitude mínima do retângulo de coordenadas"),
    lat_max: float = Query(..., description="Latitude máxima do retângulo de coordenadas"),
    lon_max: float = Query(..., description="Longitude máxima do retângulo de coordenadas")
):
    try:
        # Definir a área de interesse (ROI) usando as coordenadas passadas
        roi = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])

        # Função para mascarar nuvens usando a banda de qualidade
        def maskLandsat(image):
            qa = image.select('QA_PIXEL')  # QA_PIXEL contém informações sobre qualidade dos pixels
            cloud_shadow_bit_mask = 1 << 3  # Bit 3: sombras de nuvens
            clouds_bit_mask = 1 << 5        # Bit 5: nuvens
            mask = qa.bitwiseAnd(cloud_shadow_bit_mask).eq(0) \
                      .And(qa.bitwiseAnd(clouds_bit_mask).eq(0))  # True se não houver nuvens/sombras
            return image.updateMask(mask)

        # Coleção Landsat 8, Surface Reflectance (T1)
        collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA') \
            .filterBounds(roi) \
            .filterDate('2024-01-01', '2024-01-20') \
            .map(maskLandsat)  # Aplicar a função de mascaramento de nuvens

        # Criar um mosaico usando a mediana dos valores de pixel para suavizar bordas
        image = collection.median()
        # Parâmetros de visualização ajustados
        vis_params = {
            'bands': ['B10', 'B6'],  
            'min': 0,                    
            'max': 0.2,                 
            'gamma': 1                  
            # 'palette': ['blue', 'green', \'yellow', 'red']
        }

        # Gerar a URL dos tiles
        map_id_dict = image.getMapId(vis_params)
        tile_url = map_id_dict['tile_fetcher'].url_format

        return JSONResponse({"tile_url": tile_url})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
