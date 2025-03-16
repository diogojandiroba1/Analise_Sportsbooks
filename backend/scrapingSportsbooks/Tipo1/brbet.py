import requests
import json
from time import sleep

# URL for the BRBET API
url = "https://sb-vip.ngx.bet/event?group_type=GROUP&identifier=SUPERBRBET"

# Headers for the request
headers = {
    "accept": "application/json, text/plain, */*",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "referer": "https://www.brbet.bet.br/",
    "origin": "https://www.brbet.bet.br",  # Adicionando o cabeçalho Origin
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"  # Adicionando user-agent
}

# Path to save the JSON file
caminho_arquivo = r"/home/diogojandiroba/Analise_Sportsbooks/data/jsonCasas/dataBRBET.json"

try:
    # Make the GET request
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    
    # Parse the JSON response
    dados_json = response.json()
    print("Dados obtidos com sucesso!")
    
    # Save the JSON data to a file
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)
        print("Dados salvos com sucesso!")
        
except requests.exceptions.SSLError as e:
    print(f"Erro de SSL/TLS: {e}")
    
except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
    
except json.JSONDecodeError as e:
    print(f"Erro ao decodificar JSON: {e}")

# Optional: Add a delay if needed
# sleep(5)  # Sleep for 5 seconds