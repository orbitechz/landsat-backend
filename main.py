from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from api.classes.SentinelClient import SentinelClient
from api.classes.SatelliteDataRequest import SatelliteDataRequest

from api.routes.geolocation_router import geolocationRouter
from api.routes.geolocation_real_time import geolocationRealtime
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(geolocationRouter)
app.include_router(geolocationRealtime)

if __name__ == "__main__":
    uvicorn.run(app,host = "0.0.0.0", port=8000)  
  
# sentinel_client = SentinelClient()
# token = sentinel_client.get_valid_token()
