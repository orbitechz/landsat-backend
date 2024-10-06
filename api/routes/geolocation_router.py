from fastapi import APIRouter
import datetime

from api.classes.SentinelClient import SentinelClient
from api.services.sentinel import *

geolocationRouter = APIRouter()


sentinel_client = SentinelClient()
# sentinel_token = sentinel_client.get_valid_token()

@geolocationRouter.get("/geolocation/true-color")
async def true_color():
  bbox = [-54.649086,-25.572176,-54.533558,-25.494263]  # Exemplo de bounding box
  time_from = datetime(2017, 1, 1)
  time_to = datetime(2024, 1, 31)
  width = 512
  height = 512
  token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ3dE9hV1o2aFJJeUowbGlsYXctcWd4NzlUdm1hX3ZKZlNuMW1WNm5HX0tVIn0.eyJleHAiOjE3MjgyMjcxNDgsImlhdCI6MTcyODIyMzU0OCwianRpIjoiNWZjMGUxMGYtM2I4Ny00OTU3LWJkY2MtYjIwZTY4NDAyYWI2IiwiaXNzIjoiaHR0cHM6Ly9zZXJ2aWNlcy5zZW50aW5lbC1odWIuY29tL2F1dGgvcmVhbG1zL21haW4iLCJzdWIiOiJlMDY4MjQyZS04Y2E2LTRjNGQtOTc2Ni05Nzc4YWYzZGY3NGEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiI1MTJkZmYwNi0wNDc5LTQwOTUtYTg4OC1lY2YyOWM4MzVjMGQiLCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwiY2xpZW50SG9zdCI6IjE3Ny43My45Ny4xODIiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC01MTJkZmYwNi0wNDc5LTQwOTUtYTg4OC1lY2YyOWM4MzVjMGQiLCJjbGllbnRBZGRyZXNzIjoiMTc3LjczLjk3LjE4MiIsImNsaWVudF9pZCI6IjUxMmRmZjA2LTA0NzktNDA5NS1hODg4LWVjZjI5YzgzNWMwZCIsImFjY291bnQiOiJlNWUwODU4OC02Y2NkLTQ1NTUtYWI3My04ZjE2OGNmM2YxM2MifQ.JMPvn6NeiEdeEmMR6tf-FHJAvVVI-tE03lA0_UlWxp1KDUmLilHal1UOxp1tq8AYKpHlghFhDNcSokXVujsgP7SVoLX1-YdKg9XOr-KCUeGPosfcomj1aq7vspp_iq6Ej-FjrKJ4lH38kk_voNuywJ_NJdcnp56RRflKORr-cE2UnhoR6t49fii4vWlEeHnkjFDjPePkxsCp67LVb46BfyIJokJLlNJaUusqa2p6z-SO65OXbghEu7KIxz2NtjI_EWUvKLzar4rrXDOkrnFuoKKi7xud3gJYx60prt0BKmDSRzCflMtY6VevLLpfG6H6tOAmSW4U-xLWZQL9Es85nw"
  
  # Processa os dados e obtém a imagem como resposta binária
  image_data = await process_satellite_data(bbox, time_from, time_to, width, height, token)
  
  if image_data:
      # Converte os dados binários da imagem em um stream de BytesIO
      return StreamingResponse(BytesIO(image_data), media_type="image/png")
  else:
      print(image_data)
      return Response(status_code=500, content="Erro ao processar imagem no Sentinel Hub")