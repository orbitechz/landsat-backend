from fastapi import APIRouter
import datetime

from api.services.sentinel import *

geolocationRouter = APIRouter()

@geolocationRouter.get("/geolocation/true-color")
async def true_color():
  bbox = [-54.649086,-25.572176,-54.533558,-25.494263]  # Exemplo de bounding box
  time_from = datetime(2021, 1, 1)
  time_to = datetime(2021, 1, 31)
  width = 512
  height = 512
  
  # Processa os dados e obtém a imagem como resposta binária
  image_data = await process_satellite_data(bbox, time_from, time_to, width, height)
  
  if image_data:
      # Converte os dados binários da imagem em um stream de BytesIO
      return StreamingResponse(BytesIO(image_data), media_type="image/png")
  else:
      print(image_data)
      return Response(status_code=500, content="Erro ao processar imagem no Sentinel Hub")