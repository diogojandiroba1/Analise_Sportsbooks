from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import os

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    os.system("pip install webdriver-manager")
    from webdriver_manager.chrome import ChromeDriverManager

# Configuração do Chrome
options = Options()
options.add_argument("--headless")  # Executa sem abrir a janela do navegador
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--mute-audio")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def verificar_eventos():
    """Verifica se há eventos disponíveis na página."""
    try:
        mensagem = driver.find_element(By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div/p').text
        return "No momento não existem eventos disponíveis." not in mensagem
    except:
        return True

def coletar_odds(url, evento):
    """Coleta odds de uma página específica."""
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 10)
        event_blocks = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div')
        ))
    except:
        print(f"Nenhum evento encontrado para {evento}.")
        return []

    dados = []
    for block in event_blocks:
        try:
            apostas = block.find_elements(By.XPATH, './/div[2]/div/div[2]')
            odds = block.find_elements(By.XPATH, './/div[4]/div/app-odd/div/div')
            for aposta, odd in zip(apostas, odds):
                print(f'{evento}: {odd.text} para {aposta.text}')
                dados.append(['BETESPORTE', evento, aposta.text, odd.text])
        except Exception as e:
            print(f"Erro ao processar um bloco de apostas: {e}")
    return dados

def betesporte():
    """Coleta dados de diferentes eventos no site."""
    eventos = {
        "risco0": 'https://betesporte.bet.br/sports/desktop/sport-league/999/4200000006',
        "SUPERodd": 'https://betesporte.bet.br/sports/desktop/sport-league/999/4200000001'
    }
    dados = []
    for nome, url in eventos.items():
        dados.extend(coletar_odds(url, nome))
    return dados

def salvar_dados(dados):
    """Salva os dados coletados em um arquivo CSV."""
    if not dados:
        print("Nenhuma aposta coletada.")
        return

    caminho_csv = r'data\\csvS\\dados_apostas.csv'
    os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)

    try:
        df_existente = pd.read_csv(caminho_csv)
    except (FileNotFoundError, pd.errors.ParserError):
        df_existente = pd.DataFrame(columns=['Casa', 'Evento', 'Aposta', 'Odd', 'Data', "Link"])

    df_novo = pd.DataFrame(dados, columns=['Casa', 'Evento', 'Aposta', 'Odd', "Link"])
    df_novo['Data'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    df_completo = pd.concat([df_existente, df_novo]).drop_duplicates(subset=['Casa', 'Evento', 'Aposta'], keep='last')
    df_completo.to_csv(caminho_csv, index=False)
    print("Dados salvos no arquivo 'dados_apostas.csv'")

try:
    dados = betesporte()
    salvar_dados(dados)
except Exception as e:
    print(f"Erro: {e}")
finally:
    driver.quit()
