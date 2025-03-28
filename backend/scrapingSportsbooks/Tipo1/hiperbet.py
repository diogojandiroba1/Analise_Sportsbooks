import http.client
import json
from time import sleep

conn = http.client.HTTPSConnection("m.hiper.bet.br")

payload = ""

headers = {
    'cookie': "NCC=PTB",
    'Accept': "application/json, text/plain, */*",
    'bragiurl': "https://bragi.sportingtech.com/",
    'customorigin': "https://m.hiper.bet.br",
    'device': "m",
    'encodedbody': "eyJyZXF1ZXN0Qm9keSI6eyJzZWFzb25JZHMiOls4MDM1MjddfSwibGFuZ3VhZ2VJZCI6MjN9",
    'languageid': "23",
    'Referer': "https://m.hiper.bet.br/ptb/bet/anteposts/super-odds-multi-specials-/soccer/super-odds",
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-platform': '"Windows"',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

# Fazendo a requisição
conn.request("GET", "/api-v2/antepost-fixture/m/23/hiperbetbrasil/803527/eyJyZXF1ZXN0Qm9keSI6eyJzZWFzb25JZHMiOls4MDM1MjddfSwibGFuZ3VhZ2VJZCI6MjN9", payload, headers)

# Obtendo resposta
res = conn.getresponse()

# Lendo e tentando decodificar o JSON
try:
    data = res.read().decode("utf-8")  # Lê e decodifica a resposta
    dados_json = json.loads(data)  # Converte a string JSON em dicionário Python

    # Caminho do arquivo para salvar os dados
    caminho_arquivo = r"data\\jsonCasas\\dataHiper.json"

    # Salvando os dados no arquivo JSON
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)
        print("Dados salvos com sucesso!")

except json.JSONDecodeError as e:
    print(f"Erro ao decodificar JSON: {e}")
