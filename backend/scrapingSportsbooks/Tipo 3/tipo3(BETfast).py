import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
from time import sleep
import os

def betfast():
    with sync_playwright() as p:
        # Inicia o navegador
        browser = p.chromium.launch(headless=False)  # headless=False para ver o navegador
        page = browser.new_page()

        # Acessa a URL
        page.goto('https://betfast.bet.br/br/sportsbook/prematch#/prematch/197')
        page.wait_for_load_state('networkidle')  # Espera até que a rede esteja inativa (carregamento completo)
        page.wait_for_selector('body')  # Garante que o corpo da página foi carregado

        # Acessa o iframe
        iframe = page.query_selector('xpath=/html/body/main/iframe')

        if iframe:
            iframe_content = iframe.content_frame()
            sections = iframe_content.query_selector_all('section.prematch-matches.outright-champ')
            print(f"{len(sections)} seções encontradas.")

            dados = []
            apostas_registradas = set()

            # Lê o arquivo CSV existente para verificar apostas já registradas
            arquivo_csv = 'data/csvS/dados_apostas.csv'
            if os.path.exists(arquivo_csv):
                with open(arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        apostas_registradas.add(tuple(row[1:4]))  # Adiciona a combinação (Evento, Aposta, Odd)
            else:
                # Cria o arquivo CSV com o cabeçalho, se não existir
                with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Casa', 'Evento', 'Aposta', 'Odd', 'Data'])  # Escreve o cabeçalho

            # Itera sobre as seções
            for i, section in enumerate(sections):
                print(f"Clicando na seção {i + 1}...")
                section.click()
                sleep(1)

                match_divs = section.query_selector_all('div.match-name')
                print(f"{len(match_divs)} partidas encontradas na seção {i + 1}.")

                # Itera sobre as partidas
                for match in match_divs:
                    match.click()
                    sleep(1)

                    market_group = iframe_content.query_selector('div.market-group.with-max-bet')
                    if market_group:
                        aposta_divs = market_group.query_selector_all('div.title')
                        odds_divs = market_group.query_selector_all('span.coef')

                        if aposta_divs and odds_divs:
                            for aposta_div, odd_div in zip(aposta_divs, odds_divs):
                                aposta = aposta_div.inner_text().strip()
                                odd = odd_div.inner_text().strip()
                                partida = match.inner_text().strip()
                                data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                casa_aposta = "BetFast"

                                aposta_tuple = (casa_aposta, partida, aposta, odd, data_hora)
                                aposta_identificador = (partida, aposta, odd)

                                # Verifica duplicatas e adiciona os dados
                                if aposta_identificador not in apostas_registradas:
                                    dados.append(aposta_tuple)
                                    apostas_registradas.add(aposta_identificador)
                                else:
                                    print(f"Aposta já cadastrada: {aposta_tuple}")
                    else:
                        print("Nenhum mercado de aposta encontrado.")
        else:
            print("Iframe NÃO encontrado.")

        # Adiciona os dados no arquivo CSV
        if dados:
            with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(dados)
            print(f"{len(dados)} novas apostas adicionadas ao arquivo 'dados_apostas.csv'.")
        else:
            print("Nenhuma aposta nova encontrada.")

        # Mantém o navegador aberto até que o usuário pressione Enter
        input("Pressione Enter para fechar o navegador...")  # Não fecha imediatamente
        browser.close()

# Executa a função
betfast()