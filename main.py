from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.classes.SentinelClient import SentinelClient

from api.routes.geolocation_router import geolocationRouter
from api.routes.earthengine_router import earthengineRouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(geolocationRouter)
app.include_router(earthengineRouter)

  
  
# sentinel_client = SentinelClient()
# token = sentinel_client.get_valid_token()
