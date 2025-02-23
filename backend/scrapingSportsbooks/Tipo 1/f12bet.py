import requests

url = "https://f12.bet.br/modules/sports/ajax.php?action=get_odds&json=1&carousel=1&lid=65096&append=1&"

headers = {
    "accept": "*/*",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
    "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjE0OTM5MTciLCJhcCI6IjE1ODg3MzIyMzEiLCJpZCI6ImI0MWIxM2RkNWI2YmE0NWQiLCJ0ciI6IjZiNzIwNGI0MzQ4YzcyNjRiMTZjY2I0MjYyMTA1NjVjIiwidGkiOjE3NDAyODcxNDAyMTl9fQ==",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "traceparent": "00-6b7204b4348c7264b16ccb426210565c-b41b13dd5b6ba45d-01",
    "tracestate": "1493917@nr=0-1-1493917-1588732231-b41b13dd5b6ba45d----1740287140219",
    "x-newrelic-id": "VQIOUl9SDxABUFJSBwEEX1MC",
    "x-requested-with": "XMLHttpRequest"
}

params = {
}

# Realizando a requisição GET
response = requests.get(url, headers=headers, params=params)

# Verificando a resposta
print(response.status_code)
print(response.text)
