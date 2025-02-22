from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
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
    # Risco Zero
    url_riscoZero = 'https://betesporte.bet.br/sports/desktop/sport-league/999/4200000006'
    driver.get(url_riscoZero)

    wait = WebDriverWait(driver, 30)
    aposta_riscoZero = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[2]/div/div[2]')))
    odds_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[4]/div/app-odd/div/div')))

    for index, element in enumerate(odds_elements, start=1):
        print(f'Odd Risco Zero: {element.text} para {aposta_riscoZero[index-1].text}')
    
    sleep(5)
    
    # Super Odd
    url_super_odd = "https://betesporte.bet.br/sports/desktop/sport-league/999/4200000001"
    driver.get(url_super_odd)
       
    odds_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[4]/div/app-odd/div/div')))
    aposta_superOdd = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[2]/div/div[2]')))
    for index, element in enumerate(odds_elements, start=1):
        print(f'Super Odd: {element.text} para {aposta_superOdd[index-1].text} ')
    
    sleep(3)
        
except Exception as e:
    print(f"Erro ao acessar a página ou localizar o elemento: {e}")

finally:
    driver.quit()