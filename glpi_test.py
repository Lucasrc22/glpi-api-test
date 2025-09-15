import requests
import pandas as pd

GLPI_JSON_URL = "https://galactus.verdanadesk.com/plugins/utilsdashboards/front/ajax/graphic.json.php?token=a2835a2c0309a808e5f8d4dc11de0aa0"

def buscar_dados():
    """
    Busca os dados JSON do GLPI já autenticado via token
    e salva em CSV para integração com Power BI
    """
    response = requests.get(GLPI_JSON_URL)

    if response.status_code == 200:
        dados = response.json()
        print("Dados recebidos com sucesso!")

        if "data" in dados:
            tickets = dados["data"]
            df = pd.DataFrame(tickets)

            df.to_csv("tickets_glpi.csv", index= False, encoding= "utf-8-sig")

            print("Exportado com sucesso!")

            print(df.head())
            return df
        
        else:
            print("Não foi possível realizar a exportação")
            return None
    
    else:
        print("Não foi possível realizar a consulta!0")
if __name__ == "__main__":
    buscar_dados()
