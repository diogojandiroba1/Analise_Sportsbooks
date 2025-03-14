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

# Configuração do Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")  # Oculta logs do Chrome
chrome_options.add_argument("--disable-gpu")  # Corrige erro de renderização
chrome_options.add_argument("--disable-software-rasterizer")  # Evita conflitos gráficos
chrome_options.add_argument("--mute-audio")  # Evita áudio de anúncios indesejados

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    def verificar_eventos():
        """Verifica se há eventos disponíveis na página."""
        try:
            mensagem = driver.find_element(By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div/p').text
            if "No momento não existem eventos disponíveis." in mensagem:
                return False
        except:
            return True
        return True

    def betesporte():
        """Coleta as odds e apostas do site."""
        dados = []

        # Verifica Risco Zero
        url_riscoZero = 'https://betesporte.bet.br/sports/desktop/sport-league/999/4200000006'
        driver.get(url_riscoZero)
        sleep(3)

        if verificar_eventos():
            wait = WebDriverWait(driver, 30)
            event_blocks = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div')))

            for block in event_blocks:
                try:
                    apostas = block.find_elements(By.XPATH, './/div[2]/div/div[2]')
                    odds = block.find_elements(By.XPATH, './/div[4]/div/app-odd/div/div')

                    for aposta, odd in zip(apostas, odds):
                        print(f'Odd Risco Zero: {odd.text} para {aposta.text}')
                        dados.append(['BETESPORTE', 'risco0', aposta.text, odd.text])
                except Exception as e:
                    print(f"Erro ao processar um bloco de apostas: {e}")

        # Verifica Super Odd
        url_super_odd = "https://betesporte.bet.br/sports/desktop/sport-league/999/4200000001"
        driver.get(url_super_odd)
        sleep(3)

        if verificar_eventos():
            wait = WebDriverWait(driver, 30)
            event_blocks = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div')))

            for block in event_blocks:
                try:
                    apostas = block.find_elements(By.XPATH, './/div[2]/div/div[2]')
                    odds = block.find_elements(By.XPATH, './/div[4]/div/app-odd/div/div')

                    for aposta, odd in zip(apostas, odds):
                        print(f'Super Odd: {odd.text} para {aposta.text}')
                        dados.append(['BETESPORTE', 'SUPERodd', aposta.text, odd.text])
                except Exception as e:
                    print(f"Erro ao processar um bloco de apostas: {e}")

        if not dados:
            print("Nenhuma aposta disponível no momento.")

        return dados

    def salvar_dados(dados):
        """Salva os dados coletados em um arquivo CSV."""
        if not dados:
            return

        caminho_csv = 'data/csvS/dados_apostas.csv'

        try:
            df_existente = pd.read_csv(caminho_csv, usecols=[0, 1, 2, 3, 4])  # Garante 5 colunas
        except (FileNotFoundError, pd.errors.ParserError):
            df_existente = pd.DataFrame(columns=['Casa', 'Evento', 'Aposta', 'Odd', 'Data'])

        df_novo = pd.DataFrame(dados, columns=['Casa', 'Evento', 'Aposta', 'Odd'])
        df_novo['Data'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Remove duplicatas
        df_novo = df_novo[~df_novo.apply(lambda row: ((df_existente['Casa'] == row[0]) &
                                                       (df_existente['Evento'] == row[1]) &
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
