import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
import os

def uxbet():
    with sync_playwright() as p:
        # Inicia o navegador
        browser = p.chromium.launch(headless=False)  # headless=False para ver o navegador
        page = browser.new_page()

        # Acessa a URL
        page.goto('https://www.ux.bet.br/home/events-area/s/SUPER_ODDS')

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
        quantidade_divs = len(divs_match_list)
        print(f"Quantidade de divs com a classe 'separatorRow': {quantidade_divs}")

        # Lista para armazenar os dados extraídos
        dados = []
        apostas_registradas = set()  # Usando um set para armazenar combinações únicas (Evento, Aposta, Odd)

        # Verifica se o arquivo CSV já existe
        arquivo_csv = 'data/csvS/dados_apostas.csv'
        if os.path.exists(arquivo_csv):
            # Lê o arquivo CSV existente para verificar apostas já registradas
            with open(arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                cabecalho = next(reader, None)  # Lê o cabeçalho
                for row in reader:
                    # Adiciona a combinação (Evento, Aposta, Odd) ao set
                    apostas_registradas.add((row[1], row[2], row[3]))  # Combinação (Evento, Aposta, Odd)
        else:
            # Cria o arquivo CSV com o cabeçalho
            with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Casa', 'Evento', 'Aposta', 'Odd', 'Data'])  # Escreve o cabeçalho

        # Itera sobre as divs
        for i, div in enumerate(divs_match_list):
            print(f"Processando div {i + 1}...")

            # Localiza as partidas, apostas e odds dentro da div
            partida = div.query_selector('div.event-name span')  # Partida
            aposta = div.query_selector('div.title.font_12.weight_400.ng-star-inserted')  # Aposta
            odd = div.query_selector('div.odd.ng-star-inserted span')  # Odd

            # Verifica se todos os elementos (partida, aposta e odd) existem
            if partida and aposta and odd:
                partida_texto = partida.inner_text().strip()
                aposta_texto = aposta.inner_text().strip()
                odd_texto = odd.inner_text().strip()

                # Data e hora atual
                data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Verificação de duplicatas
                aposta_identificador = (partida_texto, aposta_texto, odd_texto)  # Combinação única para verificar duplicatas
                if aposta_identificador not in apostas_registradas:
                    # Adiciona os dados ao conjunto
                    dados.append(("UxBet", partida_texto, aposta_texto, odd_texto, data_hora))
                    apostas_registradas.add(aposta_identificador)  # Marca como registrada
                else:
                    print(f"Aposta já cadastrada: {aposta_identificador}")
            else:
                print(f"Div {i + 1} não contém todas as informações necessárias (partida, aposta, odd). Ignorando.")

        # Adiciona os dados no arquivo CSV
        if dados:
            with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(dados)  # Adiciona os dados extraídos

            print(f"{len(dados)} dados adicionados ao arquivo 'dados_apostas.csv'.")
        else:
            print("Nenhuma aposta nova encontrada.")

        # Mantém o navegador aberto até que o usuário pressione Enter

        # Fecha o navegador
        browser.close()

# Executa a função
uxbet()