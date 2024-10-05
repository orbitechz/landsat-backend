import requests
from datetime import datetime
# from api.classes.SentinelClient import SentinelClient

def process_satellite_data(
        bbox: list, 
        time_from: datetime, 
        time_to: datetime, 
        width: int, 
        height: int):
    
    sentinel_endpoint = "https://services-uswest2.sentinel-hub.com/api/v1/process"
    # sentinel_client = SentinelClient()

    # sentinel_token = sentinel_client.get_valid_token()  
    sentinel_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ3dE9hV1o2aFJJeUowbGlsYXctcWd4NzlUdm1hX3ZKZlNuMW1WNm5HX0tVIn0.eyJleHAiOjE3MjgxNjMwMjksImlhdCI6MTcyODE1OTQyOSwianRpIjoiMWUyMDYwYTgtZjhhZS00NDk0LWI4MTAtODI0MDJiN2EyZTQ4IiwiaXNzIjoiaHR0cHM6Ly9zZXJ2aWNlcy5zZW50aW5lbC1odWIuY29tL2F1dGgvcmVhbG1zL21haW4iLCJzdWIiOiJlMDY4MjQyZS04Y2E2LTRjNGQtOTc2Ni05Nzc4YWYzZGY3NGEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiI1MTJkZmYwNi0wNDc5LTQwOTUtYTg4OC1lY2YyOWM4MzVjMGQiLCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJjbGllbnRIb3N0IjoiMTc3LjczLjk3LjE4MiIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LTUxMmRmZjA2LTA0NzktNDA5NS1hODg4LWVjZjI5YzgzNWMwZCIsImNsaWVudEFkZHJlc3MiOiIxNzcuNzMuOTcuMTgyIiwiY2xpZW50X2lkIjoiNTEyZGZmMDYtMDQ3OS00MDk1LWE4ODgtZWNmMjljODM1YzBkIiwiYWNjb3VudCI6ImU1ZTA4NTg4LTZjY2QtNDU1NS1hYjczLThmMTY4Y2YzZjEzYyJ9.mnFLxbRxcDReoBAS_AiBB9im4RvYVpbaUIkhyJH5LauKrXU0gDY27VSoAWcLOr6H_r8Bw2QTwIQx06d1IRpWi63JQOVUX3eSIgioGZtXmvplQXH1BqUsGSh8jsMzyKWS9DjYZLlHRlufmarDJ09X2Bs9DJrABSAezuHa70rAk2W3B2y37MlmXMLFI5FPX-9c2EOwammMlm1owBchBSYW-Tl-VDoXrk27EJZyn0lVKS0P50R_hNID6XJZXb_P1HcWzGTZTxyHiDHgqEIVgdz7I_YUhZd37KrMYpmJl85RBcjKDVrXTRWsNz4BqACgBJll3gHSYlcRhfnlMNkc-o94uw"  

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
    
    files = {
        'request': (None, str(request_data), 'application/json'),
        'evalscript': (None, evalscript, 'text/plain'),
    }
    
    response = requests.post(sentinel_endpoint, headers=headers, files=files)
    
    if response.status_code == 200:
        return response.json()  
    else:
        return {
            "error": response.status_code,
            "message": response.text
        }
