from fastapi import Depends, FastAPI
from typing_extensions import Annotated
from functools import lru_cache
from api.utils import config

app = FastAPI()

@lru_cache
def get_settings():
    return config.Settings()


@app.get("/")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {"message": settings.auth_url}