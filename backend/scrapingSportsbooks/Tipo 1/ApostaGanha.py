from PIL import Image, ImageChops
import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests

# Função para gerar um nome de arquivo único baseado no timestamp
def generate_unique_filename(base_name):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    return f'prints/{base_name}_{timestamp}.png'

# Função para enviar imagens para o grupo no Telegram (tópico 3)
def send_image_to_telegram(bot_token, chat_id, topic_id, image_path):
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    
    with open(image_path, 'rb') as photo:
        payload = {
            'chat_id': chat_id,
            'reply_to_message_id': topic_id  # Garantindo que a imagem vai para o tópico 3
        }
        files = {'photo': photo}
        
        response = requests.post(url, data=payload, files=files)
        if response.status_code == 200:
            print(f'Imagem {image_path} enviada com sucesso para o tópico {topic_id}!')
        else:
            print(f'Falha ao enviar imagem {image_path}, status: {response.status_code}')

# Cria a pasta para salvar os prints, se não existir
os.makedirs('prints', exist_ok=True)

# Defina o token do seu bot e o chat_id do grupo
bot_token = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'
chat_id = '-1002647595950'  # ID do grupo
topic_id = 3  # ID do tópico 3

with sync_playwright() as p:
    # Inicia o navegador
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Acesse a URL do site
    page.goto('https://www.apostaganha.bet.br/esportes/odd-suprema')

    # Clica no botão de verificação
    verify_button = page.locator('xpath=/html/body/app-root/shared-ui-age-gate/div/div/ag-outline-button[2]/div/button')
    verify_button.click()

    # Aguarda 5 segundos para a página carregar completamente
    page.wait_for_timeout(5000)

    # Clica no botão de aceitar cookies
    accept_cookies_button = page.locator('xpath=/html/body/app-root/div/shared-ui-accept-cookies/div/ag-button/div/button')
    accept_cookies_button.click()

    # Aguarda um tempo para garantir que a página carregou corretamente após aceitar os cookies
    page.wait_for_timeout(3000)

    # Clicar nos ag-expansion-panel, pulando os dois primeiros
    panels = page.query_selector_all('ag-expansion-panel')
    for i, panel in enumerate(panels):
        if i >= 2:  # Pula os dois primeiros painéis
            panel.click()
            page.wait_for_timeout(2000)  # Aguarda 2 segundos para garantir que o painel foi aberto

    # Aguarda 2 segundos antes de tirar o primeiro print
    page.wait_for_timeout(3000)

    # Primeiro print da seção principal
    main_section = page.locator('section.card-highlight-bet.card-highlight-bet-odd-suprema.default')
    main_section_path = generate_unique_filename('main_section')
    main_section.screenshot(path=main_section_path)
    print(f'Nova imagem salva: {main_section_path}')
    
    # Envia a imagem para o Telegram (Tópico 3)
    send_image_to_telegram(bot_token, chat_id, topic_id, main_section_path)

    # Aguarda 2 segundos antes de iniciar os próximos passos
    page.wait_for_timeout(2000)

    # Lista para armazenar as imagens
    saved_images = [main_section_path]

    # Encontra todas as divs com a classe "container regular"
    containers = page.query_selector_all('div.container.regular')

    # Itera sobre os containers e começa a tirar prints apenas dos últimos três containers
    for i, container in enumerate(containers):
        if i < len(containers) - 3:  # Pula os primeiros containers, não tira print deles
            container.click()
            # Aguarda 3 segundos para garantir que o conteúdo foi carregado após o clique
            page.wait_for_timeout(3000)
        else:
            container.click()  # Para os últimos três containers, tira os prints
            # Aguarda 2 segundos para garantir que o conteúdo foi carregado após o clique
            page.wait_for_timeout(3000)

            # Tirar o print de todas as sections
            sections = page.query_selector_all('section.card-highlight-bet.card-highlight-bet-odd-suprema.default')
            
            for j, section in enumerate(sections):
                section_path = generate_unique_filename(f'section_{i+1}_print_{j+1}')
                section.screenshot(path=section_path)
                print(f'Nova imagem salva: {section_path}')
                saved_images.append(section_path)
                
                # Envia a imagem para o Telegram (Tópico 3)
                send_image_to_telegram(bot_token, chat_id, topic_id, section_path)

                # Aguarda 2 segundos após cada screenshot para garantir estabilidade
                page.wait_for_timeout(2000)

        # Aguarda 3 segundos entre os cliques para não sobrecarregar a página
        page.wait_for_timeout(3000)

    # Fecha o navegador
    browser.close()
