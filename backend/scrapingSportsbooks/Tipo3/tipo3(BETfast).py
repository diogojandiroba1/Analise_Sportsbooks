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
        page.wait_for_load_state('networkidle')
        page.wait_for_selector('body')

        # Acessa o iframe
        iframe = page.query_selector('xpath=/html/body/main/iframe')

        if iframe:
            iframe_content = iframe.content_frame()
            dados = []

            # Caminho do arquivo CSV
            arquivo_csv = 'data/csvS/dados_apostas.csv'

            # Verifica se o arquivo já existe
            if not os.path.exists(arquivo_csv):
                with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Casa', 'Evento', 'Aposta', 'Odd', 'Data'])  # Escreve o cabeçalho

            # Itera sobre as seções
            sections = iframe_content.query_selector_all('section.prematch-matches.outright-champ')
            for section_idx, section in enumerate(sections):
                print(f"Processando seção {section_idx + 1}...")
                section.click()
                sleep(2)

                # Encontra todas as partidas
                partidas = section.query_selector_all('ul > li')
                print(f"{len(partidas)} partidas encontradas na seção {section_idx + 1}.")

                # Expande cada partida
                for partida in partidas:
                    print(f"Expandindo partida: {partida.inner_text().strip()}...")
                    partida.click()
                    sleep(1)

                # Aguarda carregamento completo
                sleep(2)

                # Itera sobre as partidas para extrair apostas
                for partida_idx, partida in enumerate(partidas):
                    partida_nome = partida.query_selector('div.match-name').inner_text().strip()

                    # XPath dinâmico para encontrar a aposta
                    xpath_aposta = f'//*[@id="prematch-events-new"]/div[1]/div/section/section[{section_idx + 1}]/ul/li[{partida_idx + 1}]/div[4]/div[1]/div/div/div/div[1]'
                    aposta_element = iframe_content.query_selector(f'xpath={xpath_aposta}')

                    if aposta_element:
                        aposta = aposta_element.inner_text().strip()
                        odd_element = partida.query_selector('span.coef')
                        odd = odd_element.inner_text().strip() if odd_element else "N/A"
                        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        casa_aposta = "BetFast"

                        aposta_tuple = (casa_aposta, partida_nome, aposta, odd, data_hora)

                        # Verifica duplicatas diretamente no CSV
                        with open(arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
                            reader = csv.reader(file)
                            next(reader)  # Pula o cabeçalho
                            if any(row[:4] == [casa_aposta, partida_nome, aposta, odd] for row in reader):
                                print(f"Aposta já cadastrada: {aposta_tuple}")
                                continue  # Pula a inserção se já existir

                        # Adiciona ao CSV
                        dados.append(aposta_tuple)
                        print(f"Nova aposta registrada: {aposta_tuple}")
                    else:
                        print(f"Nenhuma aposta encontrada para a partida: {partida_nome}.")

        else:
            print("Iframe NÃO encontrado.")

        # Salva novas apostas no CSV
        if dados:
            with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(dados)
            print(f"{len(dados)} novas apostas adicionadas ao arquivo 'dados_apostas.csv'.")
        else:
            print("Nenhuma aposta nova encontrada.")

        # Mantém o navegador aberto até que o usuário pressione Enter
        browser.close()

# Executa a função
betfast()
