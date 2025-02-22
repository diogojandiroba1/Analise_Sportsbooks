import requests
from pathlib import Path
import json




#VERABET
url = "https://prod20350-152319086.fssb.io/api/eventlist/eu/leagues/674990359025340416/outrights"

caminho_arquivo = 'data\dataBATEUBET.json'



headers = {
    "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsYW5ndWFnZUNvZGUiOiJici1wdCIsImN1cnJlbmN5UmF0ZSI6MSwiY3VycmVuY3lSYXRlZXVyIjoxLCJjdXN0b21lckxpbWl0cyI6W10sImN1c3RvbWVyVHlwZSI6ImFub24iLCJjdXJyZW5jeUNvZGUiOiJCUkwiLCJjdXJyZW5jeUNvZGVBbm9uIjoiIiwiY3VzdG9tZXJJZCI6LTEsImJldHRpbmdWaWV3IjoiRXVyb3BlYW4gVmlldyIsInNvcnRpbmdUeXBlSWQiOjAsImJldHRpbmdMYXlvdXQiOjEsImRpc3BsYXlUeXBlSWQiOjEsInRpbWV6b25lSWQiOiIxMCIsImF1dG9UaW1lWm9uZSI6MSwibGFzdElucHV0U3Rha2UiOjAsImV1T2Rkc0lkIjoiMSIsImFzaWFuT2Rkc0lkIjoiMSIsImtvcmVhbk9kZHNJZCI6IjEiLCJpbnRUYWJFeHBhbmRlZCI6MSwiZG9tYWluSUQiOjM1NjAsImFnZW50SUQiOjE1MjMxOTA4Niwic2l0ZUlkIjoyMDM1MCwic2VsZWN0ZWRPcHRpb25JZCI6MCwiY3VzdG9tZXJMZXZlbCI6MCwiaWF0IjoxNzQwMjUxMTI3fQ.RyCkLysvde2zagkWPZ1ApxPCZflTo-pyCSTmgSexJV0",
    "accept": "application/json",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
    "priority": "u=1, i",
    "referer": "https://prod20350-152319086.fssb.io/br-pt/spbk/Especiais/Brasil/Anagaming-Specials?operatorToken=logout&navExpanded=false&selectedDefaultTab=Early&selectedEarlySport=1&selectedEarlyDayId=2025-02-22&selectedLeagueTabs=Outrights",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-fetch-storage-access": "active",
    "session": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lcklkIjotMSwiZXhwaXJlZERhdGUiOjE3NDAzMzc4NjkwNzUsImlhdCI6MTc0MDI1MTEyN30.XeJboLBYWhFjaRKmq9_dNJH1rx2rWZEi0a7_COL0BV8",
    "time-area": "",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, verify=True)  
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
    
###############################################################################################################################################################    



url = "https://prod20350-153962142.fssb.io/api/eventlist/eu/leagues/677951512097587200/outrights"

caminho_arquivo = 'data\dataBATEUBET.json'



headers = {
    "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsYW5ndWFnZUNvZGUiOiJici1wdCIsImN1cnJlbmN5UmF0ZSI6MSwiY3VycmVuY3lSYXRlZXVyIjoxLCJjdXN0b21lckxpbWl0cyI6W10sImN1c3RvbWVyVHlwZSI6ImFub24iLCJjdXJyZW5jeUNvZGUiOiJCUkwiLCJjdXJyZW5jeUNvZGVBbm9uIjoiIiwiY3VzdG9tZXJJZCI6LTEsImJldHRpbmdWaWV3IjoiRXVyb3BlYW4gVmlldyIsInNvcnRpbmdUeXBlSWQiOjAsImJldHRpbmdMYXlvdXQiOjEsImRpc3BsYXlUeXBlSWQiOjEsInRpbWV6b25lSWQiOiIxMCIsImF1dG9UaW1lWm9uZSI6MSwibGFzdElucHV0U3Rha2UiOjAsImV1T2Rkc0lkIjoiMSIsImFzaWFuT2Rkc0lkIjoiMSIsImtvcmVhbk9kZHNJZCI6IjEiLCJpbnRUYWJFeHBhbmRlZCI6MSwiZG9tYWluSUQiOjM1NjAsImFnZW50SUQiOjE1MjMxOTA4Niwic2l0ZUlkIjoyMDM1MCwic2VsZWN0ZWRPcHRpb25JZCI6MCwiY3VzdG9tZXJMZXZlbCI6MCwiaWF0IjoxNzQwMjUxMTI3fQ.RyCkLysvde2zagkWPZ1ApxPCZflTo-pyCSTmgSexJV0",
    "accept": "application/json",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
    "priority": "u=1, i",
    "referer": "https://prod20350-152319086.fssb.io/br-pt/spbk/Especiais/Brasil/Anagaming-Specials?operatorToken=logout&navExpanded=false&selectedDefaultTab=Early&selectedEarlySport=1&selectedEarlyDayId=2025-02-22&selectedLeagueTabs=Outrights",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-fetch-storage-access": "active",
    "session": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lcklkIjotMSwiZXhwaXJlZERhdGUiOjE3NDAzMzc4NjkwNzUsImlhdCI6MTc0MDI1MTEyN30.XeJboLBYWhFjaRKmq9_dNJH1rx2rWZEi0a7_COL0BV8",
    "time-area": "",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, verify=True)  
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