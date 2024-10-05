from fastapi import Depends, FastAPI
from api.classes.SentinelClient import SentinelClient

app = FastAPI()
sentinel_client = SentinelClient()
token = sentinel_client.get_valid_token()

@app.get("/")
async def info():
    return {"token": token} 