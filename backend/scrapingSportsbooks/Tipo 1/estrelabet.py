import requests
import json
from time import sleep





while True:

    #BETPIX365

    url = "https://sb2frontend-altenar2.biahosted.com/api/widget/GetOutrightEvents"
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
        "origin": "https://www.estrelabet.bet.br",
        "priority": "u=1, i",
        "referer": "https://www.estrelabet.bet.br/",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    caminho_arquivo = "data\\dataESTRELABET.json"


    try:
            response = requests.get(url, headers=headers) 
            response.raise_for_status() 
            
            dados_json = response.json()
            print("Dados obtidos com sucesso!")
            
            with open(caminho_arquivo,'w', encoding='utf-8') as arquivo:
                json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)
                print("dados salvos")
                
    except requests.exceptions.SSLError as e:
            print(f"Erro de SSL/TLS: {e}")
            
    except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            

    sleep(60)
####################################################################################################################################################################################################