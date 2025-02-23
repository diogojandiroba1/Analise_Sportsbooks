import requests
import json
from time import sleep





while True:

    #BETPIX365

    url = "https://betpix365.com/api-v2/fixture/category-details/d/23/betpix365/null/false/ante/20/super-odds-multi-specials-/soccer/super-odds"
    
    headers = {
    "accept": "application/json, text/plain, */*",
    "bragiurl": "https://bragi.sportingtech.com/",
    "customorigin": "https://betpix365.com",
    "device": "m",
    "encodedbody": "eyJyZXF1ZXN0Qm9keSI6eyJhbnRlUG9zdEV2ZW50Ijp0cnVlLCJiZXRUeXBlR3JvdXBMaW1pdCI6MjAsImJyYWdpVXJsIjoiaHR0cHM6Ly9icmFnaS5zcG9ydGluZ3RlY2guY29tLyJ9fQ==",
    "languageid": "23",
    "referer": "https://betpix365.com/ptb/bet/super-odds-multi-specials-/soccer/super-odds",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

    caminho_arquivo = "data\\dataBETPIX365.json"


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