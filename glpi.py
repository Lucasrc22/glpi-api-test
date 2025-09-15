import requests
import pandas as pd

# Endpoint direto do JSON já com token
GLPI_JSON_URL = "https://galactus.verdanadesk.com/plugins/utilsdashboards/front/ajax/graphic.json.php?token=a2835a2c0309a808e5f8d4dc11de0aa0"

def buscar_dados():
    """
    Busca os dados JSON do GLPI já autenticado via token
    e salva em CSV apenas o conteúdo da chave 'data'
    """
    response = requests.get(GLPI_JSON_URL)

    if response.status_code == 200:
        dados = response.json()

        if "data" in dados:
            tickets = dados["data"]  # pega só o que está em "data"
            df = pd.DataFrame(tickets)

            # Salva em CSV
            df.to_csv("tickets_glpi.csv", index=False, encoding="utf-8-sig")
            print("✅ Tickets exportados com sucesso para 'tickets_glpi.csv'")
            print(df.head())
            return df
        else:
            print("❌ O JSON não contém a chave 'data'")
            return None
    else:
        print(f"❌ Erro ao buscar dados. Status: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    buscar_dados()
