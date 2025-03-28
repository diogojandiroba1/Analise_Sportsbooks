import csv
import time
import os
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def betfast():
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)
    driver.get('https://mcgames.bet.br/sports#/sport/115/category/1365')
    time.sleep(10)  # Aguarde o carregamento da página
    
    dados = []
    arquivo_csv = 'data/csvS/dados_apostas.csv'
    apostas_registradas = set()

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
    odd_buttons = driver.find_elements(By.CSS_SELECTOR, '[class*="OddBox"] button')
    actions = ActionChains(driver)
    
    for button in odd_buttons:
        try:
            actions.move_to_element(button).click().perform()
            print("Clicou no botão de odd.")
            time.sleep(5)  # Aguarda o carregamento da aposta
            
            # Coletar informações da aposta
            aposta_box = driver.find_element(By.CSS_SELECTOR, '[class*="BetSlipSelectionBox"]')
            evento = aposta_box.find_element(By.CSS_SELECTOR, '[class*="EventName"]').text.strip()
            aposta = aposta_box.find_element(By.CSS_SELECTOR, '[class*="OddName"]').text.strip()
            odd = aposta_box.find_element(By.CSS_SELECTOR, '[class*="OddValue"]').text.strip()
            
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
        except Exception as e:
            print("Erro ao coletar aposta:", e)

    # Salvar os dados no CSV
    if dados:
        with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(dados)
        print(f"{len(dados)} novas apostas adicionadas ao arquivo 'dados_apostas.csv'.")
    else:
        print("Nenhuma aposta nova encontrada.")

    driver.quit()

betfast()