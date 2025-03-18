import os
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Função para enviar a imagem para o Telegram
def send_image_to_telegram(bot_token, chat_id, topic_id, image_bytes):
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'reply_to_message_id': topic_id  # Usando 'topic_id' como 'reply_to_message_id'
    }
    files = {'photo': image_bytes}

    response = requests.post(url, data=payload, files=files)
    if response.status_code == 200:
        print(f'✅ Imagem enviada para o tópico {topic_id}')
    else:
        print(f'❌ Falha ao enviar imagem, status: {response.status_code}')

# Função para capturar a tela completa e enviar para o Telegram
def tirar_print_completo(driver, bot_token, chat_id, topic_id):
    total_altura = driver.execute_script("return document.body.scrollHeight")
    viewport_altura = driver.execute_script("return window.innerHeight")
    scroll_pos = 0
    contador = 1
    
    while scroll_pos < total_altura:
        driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
        sleep(1)  # Aguardar a rolagem
        
        # Capturar a tela
        imagem_bytes = driver.get_screenshot_as_png()
        print(f"Captura de tela {contador} enviada...")
        
        # Enviar para o Telegram
        send_image_to_telegram(bot_token, chat_id, topic_id, imagem_bytes)
        
        # Rolagem pela metade da altura da janela
        scroll_pos += viewport_altura / 2
        contador += 1
        sleep(2)  # Tempo de espera entre os envios para evitar erros

# Função principal para acessar as URLs e tirar prints
def mcgames():
    urls = [
        "https://mcgames.bet.br/sports#/sport/115/category/1365/championship/50459",
        "https://mcgames.bet.br/sports#/sport/90/category/1325/championship/51072"
    ]
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Rodar sem abrir janela (opcional)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    for i, url in enumerate(urls):
        driver.get(url)
        sleep(5)  # Aguardar carregamento inicial
        
        if i == 0:
            try:
                driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div[2]/div[2]/button[2]").click()
                sleep(11)  # Esperar carregamento
            except:
                pass
        
        # Tirar print da página e enviar para o Telegram
        tirar_print_completo(driver, bot_token, chat_id, topic_id)
    
    driver.quit()

if __name__ == "__main__":
    bot_token = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'  # Substitua pelo seu token
    chat_id = '-1002647595950'  # Substitua pelo ID do grupo
    topic_id = 380  # ID do tópico correto (se necessário para agrupamento de posts)
    
    # Executar o processo 5 vezes
    for _ in range(5):
        print("Iniciando nova execução...")
        mcgames()
        sleep(5)  # Aguardar antes de iniciar a próxima execução
