import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def tirar_print(driver, nome_arquivo):
    diretorio = "prints"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    driver.save_screenshot(caminho_arquivo)
    print(f"Screenshot salvo: {caminho_arquivo}")

def mcgames():
    urls = [
        "https://mcgames.bet.br/sports#/sport/115/category/1365/championship/50459",
        "https://mcgames.bet.br/sports#/sport/90/category/1325/championship/51072"
    ]
    
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Rodar sem abrir janela (opcional)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    for i, url in enumerate(urls):
        driver.get(url)
        sleep(5)  # Aguardar carregamento inicial
        
        if i == 0:
            try:
                driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div[2]/div[2]/button[2]").click()
                sleep(25)  # Esperar carregamento
            except:
                pass
        
        tirar_print(driver, f"pagina_{i+1}.png")
    
    driver.quit()

if __name__ == "__main__":
    mcgames()
