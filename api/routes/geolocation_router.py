from fastapi import APIRouter

geolocationRouter = APIRouter()

@geolocationRouter.get("/geolocation/true-color")
async def true_color():
    return {"message": "Hello World"}
