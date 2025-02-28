import requests
import json
from time import sleep





while True:

    #UXBET

    url = "https://sb-vip8.ngx.bet/event?type=CHALLENGE&category=SUPER_ODDS&sub_type=SUPER_ODDS"
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": "Bearer a43d2dbf-08e3-4aaf-813c-081d27cd3d41",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "origin": "https://www.ux.bet.br"
    }

    caminho_arquivo = "data\\jsonCasas\\dataUXBET.json"


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