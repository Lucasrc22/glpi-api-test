# GLPI API to Power BI

**Descrição:**  
Este projeto fornece uma API simples e robusta para transformar os dados do GLPI (via CSV gerado) em JSON ou CSV, prontos para integração direta com **Power BI** ou qualquer outra ferramenta de BI.

A API é construída com **FastAPI**, totalmente compatível com **UTF-8**, e preparada para rodar em ambientes online, como **Render**, com endpoints claros para JSON e CSV.

---

## 📦 Funcionalidades

- `/` → Status da API.
- `/tickets` → Retorna os tickets em **JSON** limpo (sem NaN, UTF-8).
- `/tickets_csv` → Retorna os tickets em **CSV** pronto para o Power BI.
- Tratamento automático de valores nulos e codificação UTF-8.
- Compatível com deploy no **Render**.

---

## 🛠 Pré-requisitos

- Python 3.10+
- Pandas
- FastAPI
- Uvicorn
- Arquivo `tickets.csv` com os dados do GLPI (UTF-8)

---

## ⚡ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/glpi-api-server.git
cd glpi-api-server
