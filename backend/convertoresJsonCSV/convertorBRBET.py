import pandas as pd
import json
from datetime import datetime
from time import sleep
import os

def brbet():
    try:
        # Carregue o JSON manualmente
        with open(r'/home/diogojandiroba/Analise_Sportsbooks/data/jsonCasas/dataBRBET.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        dados = []
        dataatual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Verifica se 'data' é uma lista ou dicionário
        if isinstance(data, list):
            for item in data:
                try:
                    partida = item['question']
                    odd = item['odds']['answers'][0]['value']
                    aposta = item['odds']['answers'][0]['answer']
                    dados.append(['BRBET', partida, aposta, odd, dataatual])
                except (KeyError, IndexError) as e:
                    print(f"Erro ao processar item: {e}")
                    continue
        elif isinstance(data, dict):
            for key, item in data.items():
                try:
                    partida = item['question']
                    odd = item['odds']['answers'][0]['value']
                    aposta = item['odds']['answers'][0]['answer']
                    dados.append(['BRBET', partida, aposta, odd, dataatual])
                except (KeyError, IndexError) as e:
                    print(f"Erro ao processar item: {e}")
                    continue
        else:
            print("Formato de JSON não suportado.")
            return []
        
        return dados
    
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
        return []

def salvar_dados_sem_duplicatas(novos_dados, caminho_csv):
    # Verifica se o arquivo CSV já existe
    if os.path.exists(caminho_csv):
        # Carrega os dados existentes
        df_existente = pd.read_csv(caminho_csv)
    else:
        # Cria um DataFrame vazio se o arquivo não existir
        df_existente = pd.DataFrame(columns=['Casa', 'Evento', 'Aposta', 'Odd', 'Data'])
    
    # Converte os novos dados para DataFrame
    df_novos = pd.DataFrame(novos_dados, columns=['Casa', 'Evento', 'Aposta', 'Odd', 'Data'])
    
    # Concatena os dados existentes com os novos
    df_final = pd.concat([df_existente, df_novos], ignore_index=True)
    
    # Remove duplicatas (considerando 'Partida', 'Aposta' e 'Odd' como chave única)
    df_final.drop_duplicates(subset=['Evento', 'Aposta', 'Odd'], keep='last', inplace=True)
    
    # Salva o DataFrame final no arquivo CSV
    df_final.to_csv(caminho_csv, index=False)
    print(f"Dados salvos no arquivo '{caminho_csv}'")


dados = brbet()

if dados:
    salvar_dados_sem_duplicatas(dados, r'/home/diogojandiroba/Analise_Sportsbooks/data/csvS/dados_apostas.csv')
else:
    print("Nenhum dado foi coletado.")

