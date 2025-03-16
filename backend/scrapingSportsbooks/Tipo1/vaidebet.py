import requests
import json
from time import sleep

# URL da API
url = "https://m.vaidebet.com/api-v2/antepost-fixture/m/23/vaidebet/803527/eyJyZXF1ZXN0Qm9keSI6eyJzZWFzb25JZHMiOls4MDM1MjddfSwibGFuZ3VhZ2VJZCI6MjN9"

# Cabeçalhos ajustados
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "pt-BR,pt;q=0.7",
    "bragiurl": "https://bragi.sportingtech.com/",
    "cookie": "NCC=PTB; NCC=PTB; lang=ptb",
    "customorigin": "https://m.vaidebet.com",
    "device": "m",
    "encodedbody": "eyJyZXF1ZXN0Qm9keSI6eyJzZWFzb25JZHMiOls4MDM1MjddfSwibGFuZ3VhZ2VJZCI6MjN9",
    "languageid": "23",
    "priority": "u=1, i",
    "referer": "https://m.vaidebet.com/ptb/bet/anteposts/super-odds-multi-specials-/soccer/super-odds",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

# Caminho do arquivo JSON
caminho_arquivo = "data/jsonCasas/dataVAIDEBET.json"

try:
    # Faz a requisição GET
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

    try:
        # Tenta decodificar o JSON da resposta
        dados_json = response.json()
        print("Dados obtidos com sucesso!")

        # Salva os dados em um arquivo JSON
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)
            print("Dados salvos com sucesso!")

    except json.JSONDecodeError:
        # Se a resposta não for um JSON válido
        print("Erro: A resposta não está no formato JSON.")
        print("Conteúdo da resposta:", response.text)  # Mostra o conteúdo da resposta

except requests.exceptions.HTTPError as e:
    # Erros HTTP (4xx, 5xx)
    print(f"Erro HTTP: {e}")

except requests.exceptions.RequestException as e:
    # Outros erros de requisição
    print(f"Erro na requisição: {e}")

# Opcional: Adicionar um delay se necessário
# sleep(5)  # Aguarda 5 segundos