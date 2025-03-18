import os
import requests
from playwright.sync_api import sync_playwright
import time  # Para adicionar um tempo de espera

# Função para enviar a imagem para o Telegram, agora usando a estrutura fornecida
def send_image_to_telegram(bot_token, chat_id, topic_id, image_path):
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    
    with open(image_path, 'rb') as photo:
        payload = {
            'chat_id': chat_id,
            'reply_to_message_id': topic_id  # Usando 'topic_id' como 'reply_to_message_id'
        }
        files = {'photo': photo}
        
        response = requests.post(url, data=payload, files=files)
        if response.status_code == 200:
            print(f'✅ Imagem {image_path} enviada para o tópico {topic_id}')
        else:
            print(f'❌ Falha ao enviar imagem {image_path}, status: {response.status_code}')


# URL do site
url = "https://www.bet365.bet.br/"

# Token do bot e chat ID do Telegram
bot_token = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'  # Substitua pelo seu token
chat_id = '-1002647595950'  # Substitua pelo ID do grupo
topic_id = 186  # ID do tópico correto (se necessário para agrupamento de posts)

# Criar pasta para salvar os prints
output_folder = "prints"
os.makedirs(output_folder, exist_ok=True)

with sync_playwright() as p:
    # Abrir navegador
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url, timeout=60000)

    # Esperar até que o botão de cookies esteja disponível usando XPath
    page.locator('xpath=/html/body/div[3]/div/div[2]/div[3]').wait_for(timeout=20000)
    
    # Clicar no botão para aceitar cookies
    page.click('xpath=/html/body/div[3]/div/div[2]/div[3]')

    # Esperar os elementos carregarem após aceitar os cookies
    page.wait_for_selector('.pbb-PopularBetBuilder_BoostLogo.pbb-BetBoost', timeout=20000)

    # Buscar todas as imagens com a classe especificada
    images = page.query_selector_all('.pbb-PopularBetBuilder_BoostLogo.pbb-BetBoost')

    print(f"Encontradas {len(images)} imagens.")

    for i, img in enumerate(images):
        # Buscar a div mais próxima manualmente usando JavaScript
        parent_div = img.evaluate_handle("(el) => el.closest('.pbb-PopularBetBuilder.gl-Participant_General')")

        if parent_div:
            # Caminho para salvar o print
            screenshot_path = os.path.join(output_folder, f"bet_{i + 1}.png")

            # Tirar print da div correspondente
            parent_div.screenshot(path=screenshot_path)
            print(f"Print salvo: {screenshot_path}")

            # Enviar o print para o Telegram usando a função fornecida
            send_image_to_telegram(bot_token, chat_id, topic_id, screenshot_path)  

            # Aguardar um tempo mais longo antes de enviar o próximo
            time.sleep(2)  # Aguardar 5 segundos para evitar problemas de tempo entre os envios

    # Fechar navegador
    browser.close()
