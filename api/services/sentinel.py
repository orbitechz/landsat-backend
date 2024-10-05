import requests
from datetime import datetime

def process_satellite_data(
        access_token: str, 
        bbox: list, 
        time_from: datetime, 
        time_to: datetime, 
        width: int, 
        height: int):
    
    url = "https://services-uswest2.sentinel-hub.com/api/v1/process"
    
    # Cabeçalhos da requisição
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    # Convertendo as datas para o formato ISO 8601 (UTC)
    time_from_str = time_from.strftime("%Y-%m-%dT%H:%M:%SZ")
    time_to_str = time_to.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Dados da requisição com parâmetros customizáveis
    request_data = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "bbox": bbox  # Customizado via argumento
            },
            "data": [{
                "type": "landsat-ot-l2",
                "dataFilter": {
                    "timeRange": {
                        "from": time_from_str,  # Customizado via argumento
                        "to": time_to_str      # Customizado via argumento
                    }
                }
            }]
        },
        "output": {
            "width": width,  # Customizado via argumento
            "height": height # Customizado via argumento
        }
    }
    
    # Script de avaliação (fixo, pode ser ajustado se necessário)
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
    
    # Enviar dados como multipart/form-data
    files = {
        'request': (None, str(request_data), 'application/json'),
        'evalscript': (None, evalscript, 'text/plain'),
    }
    
    # Realiza a requisição POST
    response = requests.post(url, headers=headers, files=files)
    
    # Verifica se a resposta foi bem sucedida
    if response.status_code == 200:
        return response.json()  # Retorna os dados como JSON
    else:
        return {
            "error": response.status_code,
            "message": response.text
        }
