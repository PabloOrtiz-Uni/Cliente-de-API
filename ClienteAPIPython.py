import requests
import pandas as pd

# Definir la URL base de la API
base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Definir los parámetros de la consulta
params = {
    "format": "geojson",
    "starttime": "2024-01-01",
    "endtime": "2024-01-02",
    "minmagnitude": 5
}

# Hacer la solicitud GET a la API
response = requests.get(base_url, params=params)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Procesar la respuesta JSON
    data = response.json()
    
    # Verificar si hay características (terremotos) en los datos
    if data['features']:
        # Extraer los datos relevantes
        features = data['features']
        
        # Crear una lista de diccionarios con los datos
        earthquakes = []
        for feature in features:
            properties = feature['properties']
            earthquakes.append({
                'Magnitud': properties['mag'],
                'Lugar': properties['place'],
                'Fecha y Hora': pd.to_datetime(properties['time'], unit='ms'),
                'URL': properties['url']
            })
        
        # Crear un DataFrame de pandas
        df = pd.DataFrame(earthquakes)
        
        # Reordenar las columnas (por ejemplo, cambiando el orden a: 'Lugar', 'Magnitud', 'Fecha y Hora', 'URL')
        df = df[['Lugar', 'Magnitud', 'Fecha y Hora', 'URL']]
        
        # Imprimir la tabla de terremotos
        print(df)
    else:
        print("No se encontraron terremotos con los criterios especificados.")
else:
    print(f"Error: {response.status_code}")
