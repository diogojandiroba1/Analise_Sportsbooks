import pandas as pd
import numpy as np
import matplotlib as mpl
from time import sleep
from datetime import datetime


def uxBET():
    df = pd.read_json(r'data\dataUXBET.json', encoding='utf-8')
    data = []

    for _, row in df.iterrows():
        if isinstance(row.get("odds"), dict) and "answers" in row["odds"] and row["odds"]["answers"]:
            aposta = row["odds"]["answers"][0]["answer"]
            odd = row["odds"]["answers"][0]["value"]
        else:
            aposta, odd = None, None  

        data.append(["UXBET", row.get("question", "Desconhecido"), aposta, odd])

    return data


def salvar_dados(dados):
    caminho_csv = r'data\dados_apostas.csv'

    try:
        df_existente = pd.read_csv(caminho_csv)
    except FileNotFoundError:
        df_existente = pd.DataFrame(columns=['Casa de Apostas', 'Partida', 'Aposta', 'Odd', 'Data de Adição'])

    df_novo = pd.DataFrame(dados, columns=['Casa de Apostas', 'Partida', 'Aposta', 'Odd'])
    df_novo['Data de Adição'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Verifica duplicatas antes de adicionar ao CSV
    df_completo = pd.concat([df_existente, df_novo], ignore_index=True)
    df_completo.drop_duplicates(subset=['Casa de Apostas', 'Partida', 'Aposta'], keep="first", inplace=True)

    df_completo.to_csv(caminho_csv, index=False)
    print(f"Dados salvos no arquivo '{caminho_csv}'")


# Loop para captura de dados a cada 30 segundos
while True:
    dados = uxBET()
    salvar_dados(dados)
    sleep(30)
