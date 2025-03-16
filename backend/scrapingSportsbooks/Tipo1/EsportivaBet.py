import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from time import sleep
import requests

def enviar_imagem_para_telegram(bot_token, chat_id, photo_path, message_thread_id):
    """
    Envia uma imagem para um tópico específico no Telegram.
    :param bot_token: Token do bot do Telegram.
    :param chat_id: ID do chat/grupo.
    :param photo_path: Caminho da imagem no sistema.
    :param message_thread_id: ID do tópico (thread) para enviar a mensagem.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(photo_path, 'rb') as photo_file:
        files = {'photo': photo_file}
        data = {
            'chat_id': chat_id,
            'message_thread_id': message_thread_id  # Especifica o tópico (thread)
        }
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            print(f'Imagem enviada com sucesso para o Tópico {message_thread_id}.')
        else:
            print(f'Erro ao enviar imagem: {response.text}')

def esportivabet():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  
        page = browser.new_page()
        page.goto('https://esportiva.bet.br/sports')
        page.wait_for_selector('body')
        sleep(5)  # Aguarda o carregamento inicial da página

        # Clicar no botão de verificação fora do iframe, se existir
        try:
            verification_button = page.query_selector('.OFi5b')
            if verification_button:
                verification_button.click()
                sleep(2)  # Aguarda a verificação
        except Exception as e:
            print("Erro ao clicar na verificação:", e)

        # Acessar o iframe antes de interagir com a página
        iframe_element = page.query_selector('xpath=//*[@id="divPageLayout"]/div[3]/div[1]/div/div/iframe')
        if not iframe_element:                       
            print("Iframe não encontrado.")
            return
        iframe = iframe_element.content_frame()

        # Encontrar todos os botões com a classe 'master_fe_Banner_banner'
        buttons = iframe.query_selector_all('.master_fe_Banner_banner')
        
        # Criar pasta para salvar as imagens, se não existir
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        
        # ID do tópico 86
        message_thread_id = 86  # Substitua pelo ID correto do tópico

        # Tirar print de cada botão e salvar na pasta
        for i, button in enumerate(buttons):
            # Gerar nome único para cada imagem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f'screenshots/button_{timestamp}_{i}.png'
            button.screenshot(path=screenshot_filename)
            print(f'Screenshot salva em {screenshot_filename}')
            
            # Enviar imagem para o Telegram (no Tópico 86)
            enviar_imagem_para_telegram(bot_token, chat_id, screenshot_filename, message_thread_id)
        
        # Fechar o navegador após o processo
        browser.close()

# Defina o token do seu bot e o chat_id do grupo
bot_token = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'  # Substitua pelo token do seu bot
chat_id = '-1002647595950'  # ID do grupo

esportivabet()