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

while True:
    try:
        response = requests.get(url, headers=headers)

        # Verifica o status da resposta
        if response.status_code == 200:
            try:
                dados_json = response.json()
                print("Dados obtidos com sucesso!")

                with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                    json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)
                    print("Dados salvos!")

            except json.JSONDecodeError:
                print("Erro: A resposta não está no formato JSON.")
                print("Conteúdo da resposta:", response.text)  # Mostra o que a API retornou

        else:
            print(f"Erro HTTP {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

    sleep(60)
