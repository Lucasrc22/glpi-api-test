import requests
import csv

# URL base do seu GLPI
glpi_url = "https://galactus.verdanadesk.com/apirest.php/"

# Tokens
app_token = "2vZ1vepjdys1QlAQaCTn99J6tnuYFNWdac7a3Hvj"            # Token da aplicação (App-Token)
user_token = "T65U8hlS0DjUDszJi4vjdAbd2l4MyihKcL2Ianft" #"nS7eWeFIYtFY9NiiOwtMmxnyn5kIzmzkh36qVe7A"          # Token do usuário (Authorization)

# Headers para autenticação
headers = {
    "App-Token": app_token,
    "Authorization": f"user_token {user_token}",
    "Content-Type": "application/json",
    
}

# Criar uma sessão (opcional, mas útil para múltiplas requisições)
session_url = f"{glpi_url}/initSession"
response = requests.get(session_url, headers=headers)
session_data = response.json()

# Recuperar o token de sessão (se necessário)
session_token = session_data.get("session_token")
headers["Session-Token"] = session_token


print("\n✅ Sessão iniciada\n")

# Consultar tickets
tickets_url = f"{glpi_url}/search/Ticket"  # ou f"{glpi_url}/Ticket/{ticket_id}" para um ticket específico

params = {
    "range": "0-9999",          # até 10 mil chamados
    "forcedisplay[0]": "2",     # ID
    "forcedisplay[1]": "1",     # Nome / Assunto
    "forcedisplay[2]": "12",    # Status
    "forcedisplay[3]": "15",    # Data de abertura
    "forcedisplay[4]": "19",    # Data de solução
    "forcedisplay[5]": "5",     # Técnico responsável
    "forcedisplay[6]": "8",     # Categoria / área
    "forcedisplay[7]": "151",   # Prazo para atendimento
}
  
#Buscar status (campo 12) diferente de 5 (solucionado) e 6 (fechado) para montar backlog. Montar velocimetro 
# separando por tempo de espera data atual - data abertura (campo 15)
# niveis 0 - 10 dias, 10 a 30 dias, 30 a 60 dias, 60 a 90 dias, 90 a 120 dias, > 120 dias

#mostrar evolução do backlog nos ultimos 6 meses

#Fazer velocimetro total do TI, separar por sistemas campo'8' = Sistemas e outro por infraestrutura campo 8 = Infraestrutura 

#Buscar status (campo 12) igual 5 ou 6 de cada mês e classificar o prazo de atendimento
# % chamados atendidos no prazo = Total de chamados atendidos no prazo (comparar data limite para atendimento [151] com data de solução  [campo 19]) / Total de chamados fechados
# fazer percentual do TI geral, por área (campo 8) = Sistemas e infraestrutura, e por técnico (campo 5)

# % chamados avaliados em 5 estrelas = Total de chamados aavaliados em 5 estrelas / Total de chamados avaliados
# fazer percentual do TI geral, por área (campo 8) = Sistemas e infraestrutura, e por técnico (campo 5)

response = requests.get(tickets_url, headers=headers, params=params)



# Ver resultado
if response.status_code in [200, 206]:
    tickets = response.json()
    tickets_data = tickets.get("data", [])
    total_tickets = tickets.get("totalcount", 0)

    print(f"🔎 Total de chamados encontrados: {total_tickets}")

    # Exportar para CSV
    with open("tickets_glpi.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Cabeçalho
        writer.writerow([
            "ID",
            "Assunto",
            "Status",
            "Data Abertura",
            "Data Solução",
            "Técnico Responsável",
            "Categoria/Área",
            "Prazo Atendimento"
        ])

        # Linhas
        for ticket in tickets_data:
            writer.writerow([
                ticket.get("2"),   # ID
                ticket.get("1"),   # Assunto
                ticket.get("12"),  # Status
                ticket.get("15"),  # Data de abertura
                ticket.get("19"),  # Data de solução
                ticket.get("5"),   # Técnico
                ticket.get("8"),   # Categoria
                ticket.get("151")  # Prazo
            ])

    print("📂 Arquivo 'tickets_glpi.csv' gerado com sucesso!")

else:
    print("❌ Erro ao consultar tickets:", response.status_code, response.text)

# Encerrar sessão
requests.get(f"{glpi_url}/killSession", headers=headers)
print("🛑 Sessão encerrada")