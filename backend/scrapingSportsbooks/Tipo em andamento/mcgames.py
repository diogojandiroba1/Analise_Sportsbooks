import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
import os

def betfast():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://mcgames.bet.br/sports#/sport/115/category/1365')
        page.wait_for_load_state('networkidle')
        page.wait_for_selector('body')

        dados = []
        arquivo_csv = 'data/csvS/dados_apostas.csv'
        apostas_registradas = set()

        # Tentativa de lidar com a verificação humana
        try:
            verification_button = page.query_selector('.OFi5b')
            if verification_button:
                verification_button.click()
                page.wait_for_timeout(5000)  # Aguarda a verificação
        except Exception as e:
            print("Erro ao clicar na verificação:", e)

        page.wait_for_timeout(10000)  # Espera para carregar as odds

        # Carregar apostas registradas do CSV
        if os.path.exists(arquivo_csv):
            with open(arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Pula o cabeçalho
                for row in reader:
                    apostas_registradas.add((row[1].strip(), row[2].strip(), row[3].strip()))
        else:
            with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Casa', 'Evento', 'Aposta', 'Odd', 'Data', 'Link'])

        # Identificar os botões de odds
        odd_buttons = page.query_selector_all('[class*="OddBox"] button')
        
        for button in odd_buttons:
            button.click()
            print("Clicou no botão de odd.")
            page.wait_for_timeout(5000)  # Aguarda o carregamento da aposta
            
            # Coletar informações da aposta
            aposta_box = page.query_selector('[class*="BetSlipSelectionBox"]')
            if aposta_box:
                evento = aposta_box.query_selector('[class*="EventName"]').inner_text().strip()
                aposta = aposta_box.query_selector('[class*="OddName"]').inner_text().strip()
                odd = aposta_box.query_selector('[class*="OddValue"]').inner_text().strip()
                
                # Data e hora atual
                data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                casa_aposta = "MCGAMES"

                # Identificador único para evitar duplicatas
                aposta_identificador = (evento, aposta, odd)
                if aposta_identificador not in apostas_registradas:
                    dados.append((casa_aposta, evento, aposta, odd, data_hora, 'https://mcgames.bet.br/sports#/sport/115/category/1365'))
                    apostas_registradas.add(aposta_identificador)
                else:
                    print(f"Aposta já cadastrada: {aposta_identificador}")
            else:
                print("Nenhuma aposta encontrada para o botão de odd clicado.")

        # Salvar os dados no CSV
        if dados:
            with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(dados)
            print(f"{len(dados)} novas apostas adicionadas ao arquivo 'dados_apostas.csv'.")
        else:
            print("Nenhuma aposta nova encontrada.")

        browser.close()

betfast()