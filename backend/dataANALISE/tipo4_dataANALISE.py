import pandas as pd
import numpy as np
import os
from time import sleep
from datetime import datetime


def uxBET():
    df = pd.read_json('data\\jsonCasas\\dataUXBET.json', encoding='utf-8')
    data = []

    for _, row in df.iterrows():
        if isinstance(row.get("odds"), dict) and "answers" in row["odds"] and row["odds"]["answers"]:
            aposta = row["odds"]["answers"][0]["answer"]
            odd = row["odds"]["answers"][0]["value"]
        else:
            aposta, odd = None, None  

        data.append(["UXBET", row.get("question", "Desconhecido"), aposta, odd, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    return data


def salvar_dados(dados):
    caminho_csv = 'data\\csvS\\dados_apostas.csv'

    # Verifica se o arquivo já existe
    existe = os.path.exists(caminho_csv)

    # Salva os dados sem sobrescrever os existentes
    df_novo = pd.DataFrame(dados)
    df_novo.to_csv(caminho_csv, mode='a', header=not existe, index=False)

    print(f"Dados adicionados ao arquivo '{caminho_csv}'")


# Loop para captura de dados a cada 30 segundos
while True:
    dados = uxBET()
    salvar_dados(dados)
    sleep(30)
