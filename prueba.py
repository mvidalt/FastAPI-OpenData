from fastapi import FastAPI, HTTPException, Response
import requests
import uvicorn
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
import json



""" async def get_all_playas():
    url = "https://services1.arcgis.com/nCKYwcSONQTkPA4K/arcgis/rest/services/Playas_2015/FeatureServer/0/query?where=Provincia%20%3D%20'ILLES%20BALEARS'&outFields=*&outSR=4326&f=json"
    response = requests.get(url)
    
    if response.status_code == 200:
        playas_data = response.json()
        
        # Obtener los atributos de las playas
        playas_attributes = [playa["attributes"] for playa in playas_data["features"]]
        
        # Construir la tabla HTML
        table_html = "<table border='1'><tr>"
        headers = playas_attributes[0].keys()
        table_html += "".join(f"<th>{header}</th>" for header in headers) + "</tr>"
        for playa in playas_attributes:
            table_html += "<tr>" + "".join(f"<td>{value}</td>" for value in playa.values()) + "</tr>"
        table_html += "</table>"
        
        # Devolver la tabla HTML como respuesta
        return Response(content=table_html, media_type="text/html")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error en obtener los datos de la API")"""

app = FastAPI()

def filter_playas(playas_data, isla=None):
    filtered_playas = playas_data["features"]  # Accede a los datos de las playas
    
    # Filtra por isla si se proporciona el parámetro
    if isla:
        filtered_playas = [playa for playa in filtered_playas if playa["attributes"]["Isla"] == isla]
    
    return filtered_playas

@app.get("/")
async def get_all_playas():
    url = "https://services1.arcgis.com/nCKYwcSONQTkPA4K/arcgis/rest/services/Playas_2015/FeatureServer/0/query?where=Provincia%20%3D%20'ILLES%20BALEARS'&outFields=*&outSR=4326&f=json"
    response = requests.get(url)
    
    if response.status_code == 200:
        playas_data = response.json()
        pretty_playas_data = json.dumps(playas_data["features"], indent=4)
        colored_json = highlight(pretty_playas_data, JsonLexer(), HtmlFormatter(style="colorful"))
        return Response(content=colored_json)
    else:
        raise HTTPException(status_code=response.status_code, detail="Error en obtener los datos de la API")

@app.get("/isla/{isla_name}")
async def get_playas_by_isla(isla_name: str):
    url = "https://services1.arcgis.com/nCKYwcSONQTkPA4K/arcgis/rest/services/Playas_2015/FeatureServer/0/query?where=Provincia%20%3D%20'ILLES%20BALEARS'&outFields=*&outSR=4326&f=json"
    response = requests.get(url)
    
    if response.status_code == 200:
        playas_data = response.json()
        filtered_playas = filter_playas(playas_data, isla=isla_name)
        return filtered_playas
    else:
        raise HTTPException(status_code=response.status_code, detail="Error en obtener los datos de la API")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
