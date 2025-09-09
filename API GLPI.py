import requests
import csv

# URL base do GLPI (sem barra no final)
glpi_url = "https://galactus.verdanadesk.com/apirest.php"

# Tokens
app_token = "2vZ1vepjdys1QlAQaCTn99J6tnuYFNWdac7a3Hvj"
user_token = "T65U8hlS0DjUDszJi4vjdAbd2l4MyihKcL2Ianft"

# Headers
headers = {
    "App-Token": app_token,
    "Authorization": f"user_token {user_token}",
    "Content-Type": "application/json",
}

# Criar sessão
response = requests.get(f"{glpi_url}/initSession", headers=headers)
session_data = response.json()
session_token = session_data.get("session_token")
headers["Session-Token"] = session_token

# Map de status
status_map = {
    1: "Novo",
    2: "Em andamento (atribuído)",
    3: "Em andamento (planejado)",
    4: "Pendente",
    5: "Resolvido",
    6: "Fechado"
}

# Endpoint search
tickets_url = f"{glpi_url}/search/Ticket"

# Parâmetros obrigatórios do search
params = {
    "range": "0-9999",
    "forcedisplay[0]": "2",   # ID
    "forcedisplay[1]": "1",   # Nome (assunto)
    "forcedisplay[2]": "12",  # Status
    "forcedisplay[3]": "80",  # Entidade
    "forcedisplay[4]": "15",  # Data abertura
    "forcedisplay[5]": "19",  # Data de solução
    "forcedisplay[6]": "151", # Prazo limite
    "forcedisplay[7]": "5",   # Técnico atribuído
    "forcedisplay[8]": "8",   # Área
    "forcedisplay[9]": "7",   # Categoria
}

# Fazer a requisição
response = requests.get(tickets_url, headers=headers, params=params)

if response.status_code in [200, 206]:
    tickets = response.json()
    total_tickets = tickets.get("totalcount", 0)
    tickets_data = tickets.get("data", [])

    print(f"🔎 Total de chamados encontrados: {total_tickets}\n")

    with open("tickets.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["ID", "Assunto", "Status", "Entidade", "Área", "Categoria", "Técnico", "Abertura", "Prazo", "Solução"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for t in tickets_data:
            tecnico_id = t.get("5")
            tecnico_nome = "Não encontrado"

            # Buscar nome do técnico
            if tecnico_id:
                user_resp = requests.get(f"{glpi_url}/User/{tecnico_id}", headers=headers)
                if user_resp.status_code == 200:
                    user_data = user_resp.json()
                    tecnico_nome = f"{user_data.get('firstname', '')} {user_data.get('realname', '')}".strip()

            # Converter status de número para texto
            status_num = t.get("12")
            status_texto = status_map.get(status_num, f"Desconhecido ({status_num})")

            writer.writerow({
                "ID": t.get("2"),
                "Assunto": t.get("1"),
                "Status": status_texto,
                "Entidade": t.get("80"),
                "Área": t.get("8"),
                "Categoria": t.get("7"),
                "Técnico": tecnico_nome,
                "Abertura": t.get("15"),
                "Prazo": t.get("151"),
                "Solução": t.get("19"),
            })

    print("✅ Exportado para tickets.csv")
else:
    print("❌ Erro ao consultar tickets:", response.status_code, response.text)

# Encerrar sessão
requests.get(f"{glpi_url}/killSession", headers=headers)
