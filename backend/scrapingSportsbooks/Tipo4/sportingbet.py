import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
import os

def sportingbet():
    with sync_playwright() as p:
        # Inicia o navegador
        browser = p.chromium.launch(headless=False)  # headless=False para ver o navegador
        page = browser.new_page()

        # Acessa a URL
        page.goto('https://sports.sportingbet.bet.br/pt-br/sports')

        # Espera o carregamento do elemento desejado
        page.wait_for_selector('//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-marquee-widget[2]/ms-highlights-marquee/ms-header/div[1]/div[2]')

        # Captura o conteúdo do elemento que contém a string "Cotas Aumentadas"
        cotas_text = page.locator('//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-marquee-widget[2]/ms-highlights-marquee/ms-header/div[1]/div[2]').text_content()

        # Verifica se o texto é "Cotas Aumentadas"
        if "Cotas Aumentadas" in cotas_text:
            # Lista para armazenar os dados extraídos
            dados = []
            apostas_registradas = set()

            # Caminho do arquivo CSV
            arquivo_csv = r'data\\csvS\\dados_apostas.csv'

            # Verifica se o arquivo CSV já existe e carrega apostas registradas
            if os.path.exists(arquivo_csv):
                with open(arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Pula o cabeçalho
                    for row in reader:
                        apostas_registradas.add(tuple(row[:4]))  # Adiciona a combinação única (Casa, Evento, Aposta, Odd)
            else:
                with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Casa', 'Evento', 'Aposta', 'Odd', 'Data'])

            # Obtém os elementos <li> dentro da <ul>
            items = page.locator('//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-marquee-widget[2]/ms-highlights-marquee/ms-scroll-adapter/div/div/ul/li')
            item_count = items.count()

            # Interage com cada item dentro da lista de apostas
            for i in range(item_count):
                item = items.nth(i)  # Obtém o elemento <li> pelo índice

                # Captura os dados da aposta, evento e odd
                aposta = item.locator('div.card-market.ng-star-inserted').text_content()
                evento = item.locator('div.card-event.ng-star-inserted').text_content()
                odd = item.locator('span.custom-odds-value-style.ng-star-inserted').text_content()

                # Determina a casa de apostas (por exemplo, o nome da casa pode estar no título da página ou em outra parte do HTML)
                casa = "SportingBet"  # Isso pode ser ajustado conforme necessário, caso precise pegar de outra parte da página

                # Verifica se a aposta já foi registrada
                aposta_completa = (casa.strip(), evento.strip(), aposta.strip(), odd.strip())
                if aposta_completa not in apostas_registradas:
                    apostas_registradas.add(aposta_completa)
                    # Adiciona os dados à lista
                    dados.append([casa.strip(), evento.strip(), aposta.strip(), odd.strip(), datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

            # Adiciona os dados ao arquivo CSV
            if dados:
                with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(dados)
                print(f"{len(dados)} novas apostas adicionadas ao arquivo 'dados_apostas.csv'.")
            else:
                print("Nenhuma aposta nova encontrada.")
        else:
            print("O conteúdo não é 'Cotas Aumentadas'. Não foi executado o scraping.")

        browser.close()

# Executa a função    
sportingbet()
