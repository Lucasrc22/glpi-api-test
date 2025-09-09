import requests

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

entity_id = 1

# Consultar tickets
tickets_url = f"{glpi_url}/search/Ticket"  # ou f"{glpi_url}/Ticket/{ticket_id}" para um ticket específico

params = {
}
params["criteria[0][field]"] = "2"
params["criteria[0][searchtype]"] = "equals"
params["criteria[0][value]"] = "10631"
#params['link'] = "OR"
#params["criteria[1][field]"] = "12"
#params["criteria[1][searchtype]"] = "equals"
#params["criteria[1][value]"] = 2
params["range"]="0-10000"
  
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
if response.status_code == 200:
    tickets = response.json()
    total_tickets = tickets.get('totalcount', 0)
    total_pagina = tickets.get('count')
    tickets_data = tickets.get('data', [])
    for ticket_access in tickets_data:
        print(f"ID: {ticket_access['2']}, Status: {ticket_access['12']},Assunto: {ticket_access['1']}")
    print(tickets_data)
    print({total_tickets})
    print({total_pagina})
    #for ticket in tickets:
    #    ticket_id = ticket.get('id', 'N/A')
    #    ticket_name = ticket.get('name', 'Sem título')
    #    ticket_status = ticket.get('status', 'Status desconhecido')
    #    print(f"ID: {ticket_id}, Nome: {ticket_name}, Status: {ticket_status}")
    
    #for ticket in tickets:
        #print(f"ID: {ticket['id']}, Assunto: {ticket['name']}, Entidade: {ticket["entities_id"]}")
else:
    if response.status_code == 206:
        tickets = response.json()
        total_tickets = tickets.get('totalcount', 0)
        total_pagina = tickets.get('count')
        tickets_data = tickets.get('data', [])
        for ticket_access in tickets_data:
            print(f"ID: {ticket_access['2']}, Assunto: {ticket_access['1']}")
        print(tickets_data)
        print({total_tickets})
        print({total_pagina})
    else:
        print("Erro ao consultar tickets:", response.status_code, response.text)

# Encerrar a sessão
requests.get(f"{glpi_url}/killSession", headers=headers)