import requests
from pathlib import Path
import json
from time import sleep



while True:
    
    #VERABET
    url = "https://prod20350-152319086.fssb.io/api/eventlist/eu/leagues/674990359025340416/outrights"

    caminho_arquivo = 'data\\dataBATEUBET.json'



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



    #BATEUBET

    url = "https://prod20350-153962142.fssb.io/api/eventlist/eu/leagues/677951512097587200/outrights"

    caminho_arquivo = 'data\\dataBATEUBET.json'



    headers = {
        "authorization": "eeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsYW5ndWFnZUNvZGUiOiJici1wdCIsImN1cnJlbmN5UmF0ZSI6MSwiY3VycmVuY3lSYXRlZXVyIjoxLCJjdXN0b21lckxpbWl0cyI6W10sImN1c3RvbWVyVHlwZSI6ImFub24iLCJjdXJyZW5jeUNvZGUiOiJCUkwiLCJjdXJyZW5jeUNvZGVBbm9uIjoiIiwiY3VzdG9tZXJJZCI6LTEsImJldHRpbmdWaWV3IjoiRXVyb3BlYW4gVmlldyIsInNvcnRpbmdUeXBlSWQiOjAsImJldHRpbmdMYXlvdXQiOjEsImRpc3BsYXlUeXBlSWQiOjEsInRpbWV6b25lSWQiOiIxMCIsImF1dG9UaW1lWm9uZSI6MSwibGFzdElucHV0U3Rha2UiOjAsImV1T2Rkc0lkIjoiMSIsImFzaWFuT2Rkc0lkIjoiMSIsImtvcmVhbk9kZHNJZCI6IjEiLCJpbnRUYWJFeHBhbmRlZCI6MSwiZG9tYWluSUQiOjM3MTIsImFnZW50SUQiOjE1Mzk2MjE0Miwic2l0ZUlkIjoyMDM1MCwic2VsZWN0ZWRPcHRpb25JZCI6MCwiY3VzdG9tZXJMZXZlbCI6MCwiaWF0IjoxNzQwMjU2MjQ0fQ.ArHaX31Pr6lTL-ra0ITxvULh6v3X4UOFKg2Q54YZVTI",
        "accept": "application/json",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
        "priority": "u=1, i",
        "referer": "https://prod20350-153962142.fssb.io/br-pt/spbk/Especiais/Brasil/Super-Cota%C3%A7%C3%B5es?operatorToken=logout&navExpanded=false&selectedDefaultTab=Live&selectedLiveSport=1&selectedLeagueTabs=Outrights",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-fetch-storage-access": "active",
        "session": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lcklkIjotMSwiZXhwaXJlZERhdGUiOjE3NDAzNDI2NDkzNTEsImlhdCI6MTc0MDI1NjI0NH0.dQGREMsDzMj15NwAEW7FKd2yHFzZpojrrTzjbDfNM_Y",
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

    #CASSINOBET

    url = "https://prod20350-152319053.fssb.io/api/eventlist/eu/leagues/674990359025340416/outrights"

    caminho_arquivo = 'data\\dataCASSINOBET.json'



    headers = {
        "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsYW5ndWFnZUNvZGUiOiJici1wdCIsImJldHRpbmdWaWV3IjoiRXVyb3BlYW4gVmlldyIsInNvcnRpbmdUeXBlSWQiOjAsImJldHRpbmdMYXlvdXQiOjEsImN1c3RvbWVyVHlwZSI6InJlYWwiLCJkaXNwbGF5VHlwZUlkIjoxLCJ0aW1lem9uZUlkIjoiMTAiLCJvZGRzU3R5bGVJZCI6IiIsImFsbG93Q2hhbmdlT2RkIjowLCJpbnRUYWJFeHBhbmRlZCI6MSwiYXV0b1RpbWVab25lIjoxLCJsYXN0SW5wdXRTdGFrZSI6IjUiLCJjb3VudHJ5Q29kZSI6IkJSIiwiY3VycmVuY3lSYXRlIjowLjEzODM1MTgyNzM2MzYwNiwiY3VycmVuY3lSYXRlZXVyIjowLjE2NzA3MDI2MDA4NzE4LCJjdXN0b21lcklkIjoxNTgwNTQ5OTMsImV1T2Rkc0lkIjoiMSIsImtvcmVhbk9kZHNJZCI6IjEiLCJhc2lhbk9kZHNJZCI6IjEiLCJvcGVyYXRvclRva2VuIjoiY2Fzc2lub2JldGJyLTE0MjJkZjk1MDE1YzUyNmQ3NGZkMzNkY2E0NTM1OGQ5OTI1M2Q0MDk5MGY2NTQ4YTdlOWE2MzUwMzJkZTZjYTkiLCJiYWxhbmNlIjowLCJ0ZXN0Q3VzdG9tZXIiOjAsImN1c3RvbWVyTG9naW4iOiJjYXNzaW5vYmV0YnJfMjg0ODg0NDEiLCJjdXJyZW5jeUNvZGUiOiJCUkwiLCJjdXN0b21lckxldmVsIjowLCJhZ2VudElEIjoxNTIzMTkwNTMsImRvbWFpbklEIjozNTU4LCJzaXRlSWQiOjIwMzUwLCJleHRDdXN0b21lcklkIjoiY2Fzc2lub2JldGJyXzI4NDg4NDQxIiwiZXh0U2Vzc2lvbklkIjoiY2Fzc2lub2JldGJyLTE0MjJkZjk1MDE1YzUyNmQ3NGZkMzNkY2E0NTM1OGQ5OTI1M2Q0MDk5MGY2NTQ4YTdlOWE2MzUwMzJkZTZjYTkiLCJsZXZlbCI6MSwiaWF0IjoxNzQwMTg4NDg3LCJib251c0JhbGFuY2UiOjAsInNlbGVjdGVkT3B0aW9uSWQiOjB9.PFWfhkBFHW6q5sZFDXoALEwYC-rlefnjYlaiUmymEBI",
        "accept": "application/json",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
        "priority": "u=1, i",
        "referer": "https://prod20350-152319053.fssb.io/br-pt/spbk/Especiais/Brasil/Anagaming-Specials?operatorToken=cassinobetbr-1422df95015c526d74fd33dca45358d99253d40990f6548a7e9a635032de6ca9&navExpanded=false&selectedDefaultTab=Early&selectedLeagueTabs=Outrights",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-fetch-storage-access": "active",
        "session": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lcklkIjoxNTgwNTQ5OTMsImV4cGlyZWREYXRlIjoxNzQwMzQzOTM2OTgzLCJjdXN0b21lcklwIjoiMTc3LjM5LjU4Ljk5IiwiaWF0IjoxNzQwMjU3NTMzfQ.XfZbhalIQtCb5ISQb8yZ5T1MhoC47Wz32kyHC5HHzWs",
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

    #APOSTATUDO

    url = "https://prod20350-apo-152319128.fssb.io/api/eventlist/eu/leagues/680052790583906304/outrights"

    caminho_arquivo = 'data\\dataAPOSTATUDO.json'



    headers = {
        "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsYW5ndWFnZUNvZGUiOiJici1wdCIsImN1cnJlbmN5UmF0ZSI6MSwiY3VycmVuY3lSYXRlZXVyIjoxLCJjdXN0b21lckxpbWl0cyI6W10sImN1c3RvbWVyVHlwZSI6ImFub24iLCJjdXJyZW5jeUNvZGUiOiJCUkwiLCJjdXJyZW5jeUNvZGVBbm9uIjoiIiwiY3VzdG9tZXJJZCI6LTEsImJldHRpbmdWaWV3IjoiRXVyb3BlYW4gVmlldyIsInNvcnRpbmdUeXBlSWQiOjAsImJldHRpbmdMYXlvdXQiOjEsImRpc3BsYXlUeXBlSWQiOjEsInRpbWV6b25lSWQiOiIxMCIsImF1dG9UaW1lWm9uZSI6MSwibGFzdElucHV0U3Rha2UiOjAsImV1T2Rkc0lkIjoiMSIsImFzaWFuT2Rkc0lkIjoiMSIsImtvcmVhbk9kZHNJZCI6IjEiLCJpbnRUYWJFeHBhbmRlZCI6MSwiZG9tYWluSUQiOjM1ODQsImFnZW50SUQiOjE1MjMxOTEyOCwic2l0ZUlkIjoyMDM1MCwic2VsZWN0ZWRPcHRpb25JZCI6MCwiY3VzdG9tZXJMZXZlbCI6MCwiaWF0IjoxNzQwMjU3NzQzfQ.DyElyJ4QelkU5CulzjoWP055k8xsyD7Y6hIKwE1LjzE",
        "accept": "application/json",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
        "priority": "u=1, i",
        "referer": "https://prod20350-apo-152319128.fssb.io/br-pt/spbk/Especiais/Brasil/ApostaTudo-Specials?operatorToken=logout&navExpanded=false&selectedDefaultTab=Live&selectedLiveSport=1&selectedLeagueTabs=Outrights",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-fetch-storage-access": "active",
        "session": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lcklkIjotMSwiZXhwaXJlZERhdGUiOjE3NDAzNDQxNDc0MjMsImlhdCI6MTc0MDI1Nzc0M30.hHWWZWuwM9NtoQLsdxG1VzZ8LTNHboUsfaHCHmnSuYI",
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

    #7KBET

    url = "https://prod20350-152319626.fssb.io/api/eventlist/eu/leagues/674990359025340416/outrights"

    caminho_arquivo = 'data\\data7KBET.json'



    headers = {
        "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsYW5ndWFnZUNvZGUiOiJici1wdCIsImN1cnJlbmN5UmF0ZSI6MSwiY3VycmVuY3lSYXRlZXVyIjoxLCJjdXN0b21lckxpbWl0cyI6W10sImN1c3RvbWVyVHlwZSI6ImFub24iLCJjdXJyZW5jeUNvZGUiOiJCUkwiLCJjdXJyZW5jeUNvZGVBbm9uIjoiIiwiY3VzdG9tZXJJZCI6LTEsImJldHRpbmdWaWV3IjoiRXVyb3BlYW4gVmlldyIsInNvcnRpbmdUeXBlSWQiOjAsImJldHRpbmdMYXlvdXQiOjEsImRpc3BsYXlUeXBlSWQiOjEsInRpbWV6b25lSWQiOiIxMCIsImF1dG9UaW1lWm9uZSI6MSwibGFzdElucHV0U3Rha2UiOjAsImV1T2Rkc0lkIjoiMSIsImFzaWFuT2Rkc0lkIjoiMSIsImtvcmVhbk9kZHNJZCI6IjEiLCJpbnRUYWJFeHBhbmRlZCI6MSwiZG9tYWluSUQiOjM1OTAsImFnZW50SUQiOjE1MjMxOTYyNiwic2l0ZUlkIjoyMDM1MCwic2VsZWN0ZWRPcHRpb25JZCI6MCwiY3VzdG9tZXJMZXZlbCI6MCwiaWF0IjoxNzQwMjU4NTY1fQ.SZ0WNly8QdjsUJ5P5sEzaVAZWAsvr5bgKz9V2DtBIto",
        "accept": "application/json",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
        "priority": "u=1, i",
        "referer": "https://prod20350-152319626.fssb.io/br-pt/spbk/Especiais/Brasil/Anagaming-Specials?operatorToken=logout&navExpanded=false&selectedDefaultTab=Early&selectedLeagueTabs=Outrights",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-fetch-storage-access": "active",
        "session": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lcklkIjotMSwiZXhwaXJlZERhdGUiOjE3NDAzNDQ5Njg5NzMsImlhdCI6MTc0MDI1ODU2NX0.W2cZXr09A0jtru8912D9PLeTPe5GO0hcQ_D4YvKlTuA",
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
        
    sleep(60)
    
    ###############################################################################################################################################################    
