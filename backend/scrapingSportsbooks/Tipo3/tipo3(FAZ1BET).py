import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
from time import sleep
import os

def faz1bet():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://faz1.bet.br/br/sportsbook/prematch#/prematch/selection/197')
        page.wait_for_selector('body')

        iframe = page.query_selector('xpath=/html/body/main/iframe')
        if not iframe:
            print("Iframe NÃO encontrado.")
            browser.close()
            return

        print("Iframe encontrado!")
        iframe_content = iframe.content_frame()
        div_alvo = iframe_content.query_selector('xpath=//*[@id="prematch"]/div[2]/div[1]/div')

        if not div_alvo:
            print("Div alvo NÃO encontrada dentro do iframe.")
            browser.close()
            return

        print("Div alvo encontrada dentro do iframe!")
        divs_match_list = div_alvo.query_selector_all('div.match-list, div.match-list.is-mobile')
        print(f"Quantidade de divs encontradas: {len(divs_match_list)}")

        dados = []
        apostas_registradas = set()
        arquivo_csv = r'data\\csvS\\dados_apostas.csv'

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

        for i, div in enumerate(divs_match_list):
            li_outright_rows = div.query_selector_all('li.outright-row')
            print(f"Div {i + 1}: {len(li_outright_rows)} elementos 'outright-row' encontrados.")

            for j, li_outright_row in enumerate(li_outright_rows):
                print(f"Clicando no <li> {j + 1} da div {i + 1}...")
                li_outright_row.click()
                sleep(1)

                casa_aposta = "Faz1Bet"
                partida = li_outright_row.query_selector('p.dotted-hidden.team-name')
                partida = partida.inner_text().strip() if partida else "N/A"
                aposta = li_outright_row.query_selector('div.title')
                aposta = aposta.inner_text().strip() if aposta else "N/A"
                odds = li_outright_row.query_selector_all('span:nth-child(2)')
                odds_text = [odd.inner_text().strip() for odd in odds if odd.inner_text().strip()]
                data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                for odd in odds_text:
                    aposta_identificador = (partida, aposta, odd)
                    if aposta_identificador not in apostas_registradas:
                        dados.append((casa_aposta, partida, aposta, odd, data_hora))
                        apostas_registradas.add(aposta_identificador)
                    else:
                        print(f"Aposta já cadastrada: {aposta_identificador}")

        if dados:
            with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(dados)
            print(f"{len(dados)} novas apostas adicionadas ao CSV.")
        else:
            print("Nenhuma nova aposta encontrada.")

        browser.close()

faz1bet()

