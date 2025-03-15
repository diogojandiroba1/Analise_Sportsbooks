import requests
import json
from time import sleep


while True:

  url = "https://sb-vip.ngx.bet/event?group_type=GROUP&identifier=SUPERBRBET"
  headers = {
      "accept": "application/json, text/plain, */*",
      "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": '"Windows"',
      "referer": "https://www.brbet.bet.br/",
      "origin": "https://www.brbet.bet.br",  # Adicionando o cabeçalho Origin
  }

  response = requests.get(url, headers=headers)

  caminho_arquivo = "data/jsonCasas/dataBRBET.json"


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