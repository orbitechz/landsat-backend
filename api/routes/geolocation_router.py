from fastapi import APIRouter
import datetime

from api.services.sentinel import *

geolocationRouter = APIRouter()

@geolocationRouter.get("/geolocation/true-color")
async def true_color():
    result = process_satellite_data(bbox=["-48.478889","-27.709595","-48.451810","-27.685656"], time_from=datetime(2024, 1, 1), time_to=datetime(2024, 1, 2), width=512, height=512)
    return result