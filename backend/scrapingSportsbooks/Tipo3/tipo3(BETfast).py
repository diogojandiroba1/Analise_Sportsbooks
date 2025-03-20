import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
from time import sleep
import os

def betfast():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://betfast.bet.br/br/sportsbook/prematch#/prematch/197')
        page.wait_for_load_state('networkidle')
        page.wait_for_selector('body')

        iframe = page.query_selector('xpath=/html/body/main/iframe')
        if not iframe:
            print("Iframe NÃO encontrado.")
            browser.close()
            return

        iframe_content = iframe.content_frame()
        dados = []
        arquivo_csv = r'data\\csvS\\dados_apostas.csv'
        apostas_registradas = set()

        if os.path.exists(arquivo_csv):
            with open(arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Pula o cabeçalho
                for row in reader:
                    apostas_registradas.add((row[1].strip(), row[2].strip(), row[3].strip()))
        else:
            with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Casa', 'Evento', 'Aposta', 'Odd', 'Data', "Link"])

        sections = iframe_content.query_selector_all('section.prematch-matches.outright-champ')
        for section_idx, section in enumerate(sections):
            print(f"Processando seção {section_idx + 1}...")
            section.click()
            sleep(2)
            
            partidas = section.query_selector_all('ul > li')
            print(f"{len(partidas)} partidas encontradas na seção {section_idx + 1}.")
            
            for partida in partidas:
                partida.click()
                sleep(1)
            
            sleep(2)
            
            for partida_idx, partida in enumerate(partidas):
                partida_nome = partida.query_selector('div.match-name').inner_text().strip()
                xpath_aposta = f'//*[@id="prematch-events-new"]/div[1]/div/section/section[{section_idx + 1}]/ul/li[{partida_idx + 1}]/div[4]/div[1]/div/div/div/div[1]'
                aposta_element = iframe_content.query_selector(f'xpath={xpath_aposta}')

                if aposta_element:
                    aposta = aposta_element.inner_text().strip()
                    odd_element = partida.query_selector('span.coef')
                    odd = odd_element.inner_text().strip() if odd_element else "N/A"
                    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    casa_aposta = "BetFast"

                    aposta_identificador = (partida_nome, aposta, odd)
                    if aposta_identificador not in apostas_registradas:
                        dados.append((casa_aposta, partida_nome, aposta, odd, data_hora))
                        apostas_registradas.add(aposta_identificador)
                    else:
                        print(f"Aposta já cadastrada: {aposta_identificador}")
                else:
                    print(f"Nenhuma aposta encontrada para a partida: {partida_nome}.")

        if dados:
            with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(dados)
            print(f"{len(dados)} novas apostas adicionadas ao arquivo 'dados_apostas.csv'.")
        else:
            print("Nenhuma aposta nova encontrada.")

        browser.close()

betfast()
