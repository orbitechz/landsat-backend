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
        height: int,
        sentinel_token: str):
    
    sentinel_endpoint = "https://services-uswest2.sentinel-hub.com/api/v1/process"


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
            "height": height, 
            "responses": [{
              "identifier": "default",
              "format": {
                "type": "image/tiff"
              }
            }]
        }
    }
      
    evalscript = """
  //VERSION=3
function setup() {
    return {
      input: [{
        bands: [
          "B10"
        ]
      }],
      output: {
        bands: 1,
        sampleType: "FLOAT32"
      }
    }
  }

  function evaluatePixel(samples) {
    return [samples.B10]
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

