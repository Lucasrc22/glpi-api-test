import requests
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from io import StringIO

app = FastAPI()

# Endpoint direto do GLPI
GLPI_JSON_URL = "https://galactus.verdanadesk.com/plugins/utilsdashboards/front/ajax/graphic.json.php?token=a2835a2c0309a808e5f8d4dc11de0aa0"

def get_tickets():
    response = requests.get(GLPI_JSON_URL)
    if response.status_code == 200:
        dados = response.json()
        if "data" in dados:
            return pd.DataFrame(dados["data"])
    return pd.DataFrame()

@app.get("/")
def root():
    return {"msg": "API GLPI Galactus rodando no Render!"}

@app.get("/tickets/json")
def tickets_json():
    df = get_tickets()
    return JSONResponse(content=df.to_dict(orient="records"))

@app.get("/tickets/csv")
def tickets_csv():
    df = get_tickets()
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    csv_buffer.seek(0)
    return StreamingResponse(
        iter([csv_buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tickets_glpi.csv"}
    )
