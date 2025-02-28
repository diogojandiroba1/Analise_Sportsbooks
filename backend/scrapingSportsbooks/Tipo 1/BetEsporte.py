from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
from datetime import datetime
import os

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    os.system("pip install webdriver-manager")
    from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    def verificar_eventos():
        try:
            mensagem = driver.find_element(By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div/p').text
            if "No momento não existem eventos disponíveis." in mensagem:
                return False
        except:
            return True
        return True

    def betesporte():
        dados = []

        # Verifica Risco Zero
        url_riscoZero = 'https://betesporte.bet.br/sports/desktop/sport-league/999/4200000006'
        driver.get(url_riscoZero)
        sleep(3)

        if verificar_eventos():
            wait = WebDriverWait(driver, 30)
            aposta_riscoZero = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[2]/div/div[2]')))
            odds_elements = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[4]/div/app-odd/div/div')))

            for index, element in enumerate(odds_elements, start=1):
                print(f'Odd Risco Zero: {element.text} para {aposta_riscoZero[index-1].text}')
                dados.append(['BETESPORTE', 'risco0', aposta_riscoZero[index-1].text, element.text])

        # Verifica Super Odd
        url_super_odd = "https://betesporte.bet.br/sports/desktop/sport-league/999/4200000001"
        driver.get(url_super_odd)
        sleep(3)

        if verificar_eventos():
            wait = WebDriverWait(driver, 30)
            aposta_superOdd = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[2]/div/div[2]')))
            odds_elements = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[4]/div/app-odd/div/div')))

            for index, element in enumerate(odds_elements, start=1):
                print(f'Super Odd: {element.text} para {aposta_superOdd[index-1].text}')
                dados.append(['BETESPORTE', 'SUPERodd', aposta_superOdd[index-1].text, element.text])

        if not dados:
            print("Nenhuma aposta disponível no momento.")

        return dados

    def salvar_dados(dados):
        if not dados:
            return

        caminho_csv = 'data\csvS\dados_apostas.csv'

        try:
            df_existente = pd.read_csv(caminho_csv)
        except FileNotFoundError:
            df_existente = pd.DataFrame(columns=['Casa de Apostas', 'Partida', 'Aposta', 'Odd', 'Data de Adição'])

        df_novo = pd.DataFrame(dados)

        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_novo['Data de Adição'] = data_atual

        # Verifica duplicatas e remove
        df_novo = df_novo[~df_novo.apply(lambda row: ((df_existente['Casa de Apostas'] == row[0]) &
                                                       (df_existente['Partida'] == row[1]) &
                                                       (df_existente['Aposta'] == row[2])).any(), axis=1)]

        df_completo = pd.concat([df_existente, df_novo], ignore_index=True)
        df_completo.to_csv(caminho_csv, index=False)
        print("Dados salvos no arquivo 'dados_apostas.csv'")

    while True:
        dados = betesporte()
        salvar_dados(dados)
        sleep(30)

except Exception as e:
    print(f"Erro ao acessar a página ou localizar o elemento: {e}")

finally:
    driver.quit()
