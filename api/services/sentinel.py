import httpx
from fastapi import FastAPI, Response
from starlette.responses import StreamingResponse
from datetime import datetime
import json
from io import BytesIO

app = FastAPI()

async def process_satellite_data(
        bbox: list, 
        time_from: datetime, 
        time_to: datetime, 
        width: int, 
        height: int):
    
    sentinel_endpoint = "https://services-uswest2.sentinel-hub.com/api/v1/process"
    sentinel_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ3dE9hV1o2aFJJeUowbGlsYXctcWd4NzlUdm1hX3ZKZlNuMW1WNm5HX0tVIn0.eyJleHAiOjE3MjgxNjY1ODMsImlhdCI6MTcyODE2Mjk4MywianRpIjoiM2ViMzc1ZjAtYmNkZi00M2UyLWEwOTQtMDc4Y2ZmMjBmNzE0IiwiaXNzIjoiaHR0cHM6Ly9zZXJ2aWNlcy5zZW50aW5lbC1odWIuY29tL2F1dGgvcmVhbG1zL21haW4iLCJzdWIiOiJlMDY4MjQyZS04Y2E2LTRjNGQtOTc2Ni05Nzc4YWYzZGY3NGEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiI1MTJkZmYwNi0wNDc5LTQwOTUtYTg4OC1lY2YyOWM4MzVjMGQiLCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJjbGllbnRIb3N0IjoiMTc3LjczLjk3LjE4MiIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LTUxMmRmZjA2LTA0NzktNDA5NS1hODg4LWVjZjI5YzgzNWMwZCIsImNsaWVudEFkZHJlc3MiOiIxNzcuNzMuOTcuMTgyIiwiY2xpZW50X2lkIjoiNTEyZGZmMDYtMDQ3OS00MDk1LWE4ODgtZWNmMjljODM1YzBkIiwiYWNjb3VudCI6ImU1ZTA4NTg4LTZjY2QtNDU1NS1hYjczLThmMTY4Y2YzZjEzYyJ9.aV90x-0m83CtJ2G7AXlGrkJYAUcwLxchn-bdm92qEVnHRt2p1s7QS6SIW1SYlM7sPghTsfM4RAEEAH1C-mNXWXXPSMQNpJDqjOGDP9fok9dj2ULimwt0__Wu538kWFfaYaQs4OCJ3cz3LxuF3Vk38ItuIcZRvrdXHTu1Duv_Q2IORo-2NomegFyF4s_cQTShy6a8Tx18nzfqayKmmHHcIycoqIOGET5nla_KUSgg5Qr8M628voz6NaWbN4q4G0Snne1LFpMgj9cUK5bdBx60wiFxXYvRSOiedlFm_JuFPIZhpMLOy4dIiOFttJABD4EwhTmUcDONF4evZXeX5m7fVw"

    headers = {
        'Authorization': f'Bearer {sentinel_token}',
    }
    
    time_from_str = time_from.strftime("%Y-%m-%dT%H:%M:%SZ")
    time_to_str = time_to.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    request_data = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "bbox": bbox  
            },
            "data": [{
                "type": "landsat-ot-l2",
                "dataFilter": {
                    "timeRange": {
                        "from": time_from_str, 
                        "to": time_to_str     
                    }
                }
            }]
        },
        "output": {
            "width": width, 
            "height": height 
        }
    }
    
    evalscript = """
    //VERSION=3

    function setup() {
        return {
            input: ["B02", "B03", "B04"],
            output: {
                bands: 3,
                sampleType: "AUTO" // default value - scales the output values from [0,1] to [0,255].
            }
        };
    }

    function evaluatePixel(sample) {
        return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
    }
    """
    
    request_data_json = json.dumps(request_data)

    files = {
        'request': (None, request_data_json, 'application/json'),  # Enviar request_data como JSON
        'evalscript': (None, evalscript, 'text/plain'),  # Enviar evalscript como texto
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            sentinel_endpoint, 
            headers=headers, 
            files=files
        )
        print(response.content)
        if response.status_code == 200:
            # Retorna os dados binários da imagem
            return response.content
        else:
            return None

