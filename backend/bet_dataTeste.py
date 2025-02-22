import pandas as pd
import numpy as np
import matplotlib as mpl
from time import sleep
from datetime import datetime

def seteKBET():
    df = pd.read_json(r'data\data7KBET.json', encoding='utf-8')
    qtd = len(df["data"])
    data = []
    print("\n7KBET\n")
    
    for acc in range(qtd):
        partida = df["data"][acc][10]
        odd = df["data"][acc][19][0][7][1][4]
        aposta = df["data"][acc][19][0][7][1][1]["BR-PT"]
        data.append(['7KBET', partida, aposta, odd])

    return data


def apostaTudo():
    df = pd.read_json(r'data\dataAPOSTATUDO.json', encoding='utf-8')
    qtd = len(df["data"])
    data = []
    print("\nAPOSTATUDO\n")
    
    for acc1 in range(qtd):
        partida = df["data"][acc1][10]
        odd = df["data"][acc1][19][0][7][0][4]
        aposta = df["data"][acc1][19][0][7][0][1]["BR-PT"]
        if odd != 0 and aposta != "Não":
            data.append(['APOSTATUDO', partida, aposta, odd])
    
    for acc2 in range(qtd):
        partida = df["data"][acc2][10]
        odd = df["data"][acc2][19][0][7][1][4]
        aposta = df["data"][acc2][19][0][7][1][1]["BR-PT"]
        if odd != 0 and aposta != "Não":
            data.append(['APOSTATUDO', partida, aposta, odd])

    return data


def bateuBET():
    df = pd.read_json(r'data\dataBATEUBET.json', encoding='utf-8')
    qtd = len(df["data"])
    data = []
    print("\nBATEUBET\n")
    
    for acc in range(qtd):
        partida = df["data"][acc][10]
        odd = df["data"][acc][19][0][7][1][4]
        aposta = df["data"][acc][19][0][7][1][1]["BR-PT"]
        data.append(['BATEUBET', partida, aposta, odd])

    return data


def cassinoBET():
    df = pd.read_json(r'data\dataCASSINOBET.json', encoding='utf-8')
    qtd = len(df["data"])
    data = []
    print("\nCASSINOBET\n")
    
    for acc in range(qtd):
        partida = df["data"][acc][10]
        odd = df["data"][acc][19][0][7][1][4]
        aposta = df["data"][acc][19][0][7][1][1]["BR-PT"]
        data.append(['CASSINOBET', partida, aposta, odd])

    return data


def veraBET():
    df = pd.read_json(r'data\dataVERABET.json', encoding='utf-8')
    qtd = len(df["data"])
    data = []
    print("\nVERABET\n")
    
    for acc in range(qtd):
        partida = df["data"][acc][10]
        odd = df["data"][acc][19][0][7][1][4]
        aposta = df["data"][acc][19][0][7][1][1]["BR-PT"]
        data.append(['VERABET', partida, aposta, odd])

    return data


def salvar_dados(dados):
    try:
        # Carregar dados existentes no CSV, se houver
        df_existente = pd.read_csv(r'data\dados_apostas.csv')
    except FileNotFoundError:
        # Se não houver o arquivo, criar um DataFrame vazio
        df_existente = pd.DataFrame(columns=['Casa de Apostas', 'Partida', 'Aposta', 'Odd', 'Data de Adição'])
    
    # Criar DataFrame com os novos dados
    df_novo = pd.DataFrame(dados, columns=['Casa de Apostas', 'Partida', 'Aposta', 'Odd'])
    
    # Obter data e hora atual
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Adicionar a coluna 'Data de Adição' a cada linha
    df_novo['Data de Adição'] = data_atual
    
    # Verificar se a aposta já foi adicionada (comparar Casa de Apostas, Partida e Aposta)
    for index, row in df_novo.iterrows():
        if ((df_existente['Casa de Apostas'] == row['Casa de Apostas']) &
            (df_existente['Partida'] == row['Partida']) &
            (df_existente['Aposta'] == row['Aposta'])).any():
            df_novo = df_novo.drop(index)
    
    # Combinar os dados existentes com os novos
    df_completo = pd.concat([df_existente, df_novo], ignore_index=True)
    
    # Salvar no CSV
    df_completo.to_csv(r'data\dados_apostas.csv', index=False)
    print("Dados salvos no arquivo 'dados_apostas.csv'")


while True:

    dados = []
    dados += seteKBET()
    dados += apostaTudo()
    dados += bateuBET()
    dados += cassinoBET()
    dados += veraBET()

    # Salvar os dados no CSV com verificação de apostas já adicionadas
    salvar_dados(dados)
    
    sleep(30)
