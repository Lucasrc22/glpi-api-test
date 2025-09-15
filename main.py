from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse, PlainTextResponse
import pandas as pd
import json
import os

app = FastAPI(title="GLPI API to PowerBI", version="1.0")

CSV_FILE = "tickets.csv"

def load_dataframe():
    """Carrega o CSV em UTF-8 e garante que não quebre se estiver vazio ou ausente"""
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame()  # retorna vazio se não existe

    try:
        df = pd.read_csv(CSV_FILE, encoding="utf-8")
        df = df.fillna("")  # substitui NaN por string vazia
        return df
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return pd.DataFrame()

@app.get("/")
def root():
    return {"message": "API GLPI -> Power BI rodando com FastAPI 🚀"}

@app.get("/tickets")
def tickets_json():
    """Retorna os dados do CSV em formato JSON seguro (sem NaN, em UTF-8)"""
    df = load_dataframe()
    data = df.to_dict(orient="records")

    try:
        json_data = json.dumps(data, ensure_ascii=False, allow_nan=False)
    except ValueError:
        # fallback em caso de erro de serialização
        json_data = json.dumps([], ensure_ascii=False)

    return Response(content=json_data, media_type="application/json; charset=utf-8")

@app.get("/tickets_csv")
def tickets_csv():
    """Retorna os dados do CSV em formato CSV puro, para consumo direto no Power BI"""
    df = load_dataframe()

    if df.empty:
        return PlainTextResponse("arquivo CSV vazio ou não encontrado", status_code=404)

    csv_data = df.to_csv(index=False, encoding="utf-8")
    return Response(content=csv_data, media_type="text/csv; charset=utf-8")
