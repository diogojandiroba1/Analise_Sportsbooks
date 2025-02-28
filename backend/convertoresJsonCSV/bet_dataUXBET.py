import pandas as pd
import os
from time import sleep
from datetime import datetime

# Carregar os dados do JSON
df = pd.read_json('data\\jsonCasas\\dataUXBET.json', encoding='utf-8')

qtd = len(df)
data = []

for acc in range(qtd):
    partida = df["question"][acc]
    odd = df["odds"][acc]["answers"][0]["value"]
    aposta = df["odds"][acc]["answers"][0]["answer"]
    
    # Capturar data e hora atuais
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data.append(['UXBET', partida, aposta, odd, data_hora])

df_final = pd.DataFrame(data, columns=['Casa de Apostas', 'Partida', 'Aposta', 'Odd', 'Data e Hora'])

# Caminho do arquivo CSV
csv_path = 'data\\csvS\\dados_apostas.csv'

# Verificar se o arquivo já existe
if os.path.exists(csv_path):
    # Carregar os dados existentes com a codificação correta
    try:
        df_existente = pd.read_csv(csv_path, encoding='ISO-8859-1')

        # Concatenar os novos dados sem duplicatas
        df_final = pd.concat([df_existente, df_final], ignore_index=True).drop_duplicates()

    except Exception as e:
        print(f"Erro ao carregar o arquivo existente: {e}")
else:
    print(f"O arquivo {csv_path} não existe. Criando um novo.")

# Salvar o arquivo CSV com cabeçalho e codificação correta
try:
    df_final.to_csv(csv_path, index=False, header=True, encoding='ISO-8859-1')
    print("Dados salvos no arquivo 'dados_apostas.csv'")
except Exception as e:
    print(f"Erro ao salvar o arquivo CSV: {e}")

sleep(30)
