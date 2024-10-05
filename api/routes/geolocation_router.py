from fastapi import APIRouter

geolocationRouter = APIRouter()

@geolocationRouter.get("/geolocation/true-color")
async def teste():
    return {"message": "Hello World"}
