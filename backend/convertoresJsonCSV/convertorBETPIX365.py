import pandas as pd
import json
from datetime import datetime
from time import sleep
import os

def betpix365():
    try:
        # Carregue o JSON manualmente
        with open(r'data\jsonCasas\dataBETPIX365.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Normalize o JSON para acessar os dados corretamente
        partidas = data['data'][0]['cs'][0]['sns'][0]['fs']
        dados = []
        dataatual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for partida in partidas:
            try:
                nome_partida = partida['hcN']
                for btg in partida['btgs']:
                    for fo in btg['fos']:
                        aposta = fo['btN']
                        odd = fo['hO']
                        dados.append(['BETPIX365', nome_partida, aposta, odd, dataatual])
            except (KeyError, IndexError) as e:
                print(f"Erro ao processar partida: {e}")
                continue
        
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
    
    # Remove duplicatas (considerando 'Evento', 'Aposta' e 'Odd' como chave única)
    df_final.drop_duplicates(subset=['Evento', 'Aposta', 'Odd'], keep='last', inplace=True)
    
    # Salva o DataFrame final no arquivo CSV
    df_final.to_csv(caminho_csv, index=False)
    print(f"Dados salvos no arquivo '{caminho_csv}'")

while True:
    dados = betpix365()

    if dados:
        salvar_dados_sem_duplicatas(dados, r'data\csvS\dados_apostas.csv')
    else:
        print("Nenhum dado foi coletado.")

    sleep(30)