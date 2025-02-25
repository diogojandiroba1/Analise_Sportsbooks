import requests
from bs4 import BeautifulSoup
import json

# URL da página que contém as partidas
url = 'https://faz1.bet.br/br/sportsbook/prematch#/prematch/selection/197'

# Fazendo a requisição para obter o conteúdo da página
response = requests.get(url)
html_content = response.content

# Parsing do HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Encontrando todas as divs na classe 'user-matches'
matches_div = soup.find_all(class_='user-matches')

# Extraindo informações das partidas
matches_list = []
for div in matches_div:
    # Supondo que cada partida está dentro de uma div com uma classe específica, por exemplo 'match'
    matches = div.find_all(class_='match-list is-mobile')
    for match in matches:
        match_info = {
            'team1': match.find(class_='team1').text.strip(),
            'team2': match.find(class_='team2').text.strip(),
            'time': match.find(class_='time').text.strip(),
            # Adicione mais campos conforme necessário
        }
        matches_list.append(match_info)

# Salvando as partidas em um arquivo JSON
with open('matches.json', 'w', encoding='utf-8') as f:
    json.dump(matches_list, f, ensure_ascii=False, indent=4)

print("Partidas salvas em matches.json")