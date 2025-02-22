import requests

# URL do endpoint
url = "https://sb-vip8.ngx.bet/event?type=CHALLENGE&category=SUPER_ODDS&sub_type=SUPER_ODDS"

# Cabeçalhos da requisição
headers = {
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.ux.bet.br/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
}

# Fazendo a requisição GET
response = requests.get(url, headers=headers)

# Verificando o status e o conteúdo da resposta
if response.status_code == 200:
    print("Requisição bem-sucedida!")
    print(response.json())  # Exibe a resposta em formato JSON
else:
    print(f"Falha na requisição. Status Code: {response.status_code}")
