from fastapi import FastAPI, Response
from starlette.responses import PlainTextResponse

import pandas as pd
import requests
import json

app = FastAPI(title="GLPI API to PowerBI", version="1.0")

# Token e URL do GLPI
GLPI_JSON_URL = "https://galactus.verdanadesk.com/plugins/utilsdashboards/front/ajax/graphic.json.php?token=a2835a2c0309a808e5f8d4dc11de0aa0"

def fetch_glpi_data():
    """
    Busca os dados diretamente do GLPI e retorna um DataFrame
    """
    try:
        response = requests.get(GLPI_JSON_URL, timeout=10)
        response.raise_for_status()  # levanta erro se status != 200
        dados = response.json()
        if "data" in dados:
            df = pd.DataFrame(dados["data"])
            df = df.fillna("")  # Remove NaN
            return df
    except requests.RequestException as e:
        print(f"Erro ao buscar dados do GLPI: {e}")
    except ValueError as e:
        print(f"Erro ao processar JSON do GLPI: {e}")
    return pd.DataFrame()  # Retorna vazio em caso de erro

@app.get("/")
def root():
    return {"message": "API GLPI -> Power BI rodando com FastAPI 🚀"}

@app.get("/tickets")
def tickets_json():
    """Retorna dados em JSON limpo, UTF-8"""
    df = fetch_glpi_data()
    data = df.to_dict(orient="records")

    try:
        json_data = json.dumps(data, ensure_ascii=False, allow_nan=False)
    except ValueError:
        json_data = json.dumps([], ensure_ascii=False)

    return Response(content=json_data, media_type="application/json; charset=utf-8")

@app.get("/tickets_csv")
def tickets_csv():
    """Retorna dados em CSV, UTF-8, pronto para Power BI"""
    df = fetch_glpi_data()

    if df.empty:
        return PlainTextResponse("Nenhum dado encontrado no GLPI", status_code=404)

    csv_data = df.to_csv(index=False, encoding="utf-8-sig")
    return Response(content=csv_data, media_type="text/csv; charset=utf-8")
