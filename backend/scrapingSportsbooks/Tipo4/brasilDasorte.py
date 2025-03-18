import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
import os

def BrasilDaSorte():
    with sync_playwright() as p:
        # Inicia o navegador
        browser = p.chromium.launch(headless=True)  # headless=False para ver o navegador
        page = browser.new_page()

        # Acessa a URL
        page.goto('https://www.brasildasorte.bet.br/home/events-area/s/SUPER_ODDS')

        # Aguarda o carregamento completo da página
        try:
            page.wait_for_selector('div.separatorRow', timeout=60000)  # Espera até 60 segundos
        except Exception as e:
            print(f"Erro ao esperar pelo seletor: {e}")
            browser.close()
            return

        print("Div alvo encontrada!")
        # Encontra todas as divs com a classe "separatorRow" que contém as apostas
        divs_match_list = page.query_selector_all('div.separatorRow')
        print(f"Quantidade de divs com a classe 'separatorRow': {len(divs_match_list)}")

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

        # Itera sobre as divs
        for div in divs_match_list:
            partida = div.query_selector('div.event-name span')
            aposta = div.query_selector('div.title.font_12.weight_400.ng-star-inserted')
            odd = div.query_selector('div.odd.ng-star-inserted span')

            if partida and aposta and odd:
                partida_texto = partida.inner_text().strip()
                aposta_texto = aposta.inner_text().strip()
                odd_texto = odd.inner_text().strip()
                data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                aposta_tuple = ("BrasilDaSorte", partida_texto, aposta_texto, odd_texto, data_hora)
                aposta_identificador = ("BrasilDaSorte", partida_texto, aposta_texto, odd_texto)

                if aposta_identificador not in apostas_registradas:
                    dados.append(aposta_tuple)
                    apostas_registradas.add(aposta_identificador)
                else:
                    print(f"Aposta já cadastrada: {aposta_identificador}")
            else:
                print("Informações incompletas, ignorando aposta.")

        # Adiciona os dados ao arquivo CSV
        if dados:
            with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(dados)
            print(f"{len(dados)} novas apostas adicionadas ao arquivo 'dados_apostas.csv'.")
        else:
            print("Nenhuma aposta nova encontrada.")

        browser.close()

# Executa a função  
BrasilDaSorte()