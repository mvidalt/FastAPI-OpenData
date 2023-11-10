import random
from fastapi import FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
import json
import json, typing
from starlette.responses import Response
from fastapi import FastAPI, HTTPException, Response, Path
import requests
import json
import typing

app = FastAPI()


class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")


app = FastAPI()

def get_all_playas_data():
    url = "https://services1.arcgis.com/nCKYwcSONQTkPA4K/arcgis/rest/services/Playas_2015/FeatureServer/0/query?where=Provincia%20%3D%20'ILLES%20BALEARS'&outFields=*&outSR=4326&f=json"
    response = requests.get(url)

    if response.status_code == 200:
        playas_data = response.json()["features"]
        return playas_data
    else:
        raise HTTPException(status_code=response.status_code, detail="Error en obtener los datos de la API")

def generate_html_table(playas_data):
    css_link = "<link rel='stylesheet' href='/static/styles.css'>"
    table_html = f"{css_link}<table border='1'><tr>"
    headers = playas_data[0].keys()
    table_html += "".join(f"<th>{header}</th>" for header in headers) + "</tr>"
    for playa in playas_data:
        table_html += "<tr>" + "".join(f"<td>{value}</td>" for value in playa.values()) + "</tr>"
    table_html += "</table>"
    return table_html



@app.get("/")
async def get_all_playas():
    playas_data = get_all_playas_data()
    
    playas_attributes = [playa["attributes"] for playa in playas_data]
    table_html = generate_html_table(playas_attributes)
    return Response(content=table_html, media_type="text/html")


@app.get("/isla/{isla}", response_class=PrettyJSONResponse)
async def get_playas_by_isla(isla: str = Path(..., title="Nombre de la isla")):
    playas_data = get_all_playas_data()
    filtered_playas = []
    for playa in playas_data:
        if playa["attributes"]["Isla"] == isla:
            filtered_playas.append(playa["attributes"])
    table_html = generate_html_table(filtered_playas)
    return Response(content=table_html, media_type="text/html")

@app.get("/conteo/{isla}", response_model=int)
async def count_playas_by_isla(isla: str = Path(..., title="Nombre de la isla")):
    playas_data = get_all_playas_data()
    
    count = 0
    for playa in playas_data:
        if playa["attributes"]["Isla"] == isla:
            count += 1
    
    return count

@app.get("/estadisticas",response_class=PrettyJSONResponse)
async def estadisticas():
    playas_data = get_all_playas_data()
    total_playas = len(playas_data)
    islas = set(playa["attributes"]["Isla"] for playa in playas_data)
    longitud_promedio = sum(float(playa["attributes"]["Longitud"].split()[0]) for playa in playas_data) / total_playas
    servicios_disponibles = ["Aseos", "Duchas", "Teléfonos", "Papelera"]
    servicios_counts = {servicio: sum(1 for playa in playas_data if playa["attributes"][servicio] == "Sí") for servicio in servicios_disponibles}
    playa_aleatoria = random.choice(playas_data)["attributes"]["Nombre"]

    # Construir la tabla HTML
    table_html = """
        <table border='1'>
            <tr>
                <th>Estadística</th>
                <th>Valor</th>
            </tr>
            <tr>
                <td>Total de Playas</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Islas</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Longitud Promedio</td>
                <td>{:.2f} metros</td>
            </tr>
            <tr>
                <td>Servicios Disponibles</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Playa Aleatoria</td>
                <td>{}</td>
            </tr>
        </table>
    """.format(total_playas, ", ".join(islas), longitud_promedio, ", ".join([f"{key} ({value})" for key, value in servicios_counts.items()]), playa_aleatoria)

    return Response(content=table_html, media_type="text/html")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/index.html")
async def index():
    html = open("index.html", "r", encoding="utf-8").read()
    return Response(content=html, media_type="text/html")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)