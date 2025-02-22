from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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
    url = 'https://betesporte.bet.br/sports/desktop/sport-league/999/4200000006'
    driver.get(url)

    wait = WebDriverWait(driver, 30)  
    odds_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[4]/div/app-odd/div/div')))

    for index, element in enumerate(odds_elements, start=1):
        print(f'Odd {index}: {element.text}')

except Exception as e:
    print(f"Erro ao acessar a página ou localizar o elemento: {e}")

finally:
    driver.quit()