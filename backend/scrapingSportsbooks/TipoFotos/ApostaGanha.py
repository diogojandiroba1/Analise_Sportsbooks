import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests

# Função para gerar um nome de arquivo único baseado no timestamp
def generate_unique_filename(base_name):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    return f'prints/{base_name}_{timestamp}.png'

# Função para enviar imagens para o grupo no Telegram
def send_image_to_telegram(bot_token, chat_id, topic_id, image_path):
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    
    with open(image_path, 'rb') as photo:
        payload = {
            'chat_id': chat_id,
            'reply_to_message_id': topic_id
        }
        files = {'photo': photo}
        
        response = requests.post(url, data=payload, files=files)
        if response.status_code == 200:
            print(f'✅ Imagem {image_path} enviada para o tópico {topic_id}')
        else:
            print(f'❌ Falha ao enviar imagem {image_path}, status: {response.status_code}')

# Criar pasta para prints
os.makedirs('prints', exist_ok=True)

# Definições do bot e grupo Telegram
bot_token = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'  # Substitua pelo seu token
chat_id = '-1002647595950'  # Substitua pelo ID do grupo
topic_id = 3  # ID do tópico correto

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Acesse a URL
    page.goto('https://www.apostaganha.bet.br/esportes/odd-suprema', timeout=60000)

    # Aguarde botão de verificação e clique
    verify_button = page.locator('xpath=/html/body/app-root/shared-ui-age-gate/div/div/ag-outline-button[2]/div/button')
    verify_button.wait_for(state="visible", timeout=10000)
    verify_button.click()

    # Aguarde a página carregar
    page.wait_for_timeout(5000)

    # Aceitar cookies
    accept_cookies_button = page.locator('xpath=/html/body/app-root/div/shared-ui-accept-cookies/div/ag-button/div/button')
    if accept_cookies_button.is_visible():
        accept_cookies_button.click()
        page.wait_for_timeout(3000)

    # Expande os painéis (pulando os dois primeiros)
    panels = page.locator('ag-expansion-panel').all()
    for i, panel in enumerate(panels):
        if i >= 2:
            panel.scroll_into_view_if_needed()
            panel.click()
            page.wait_for_timeout(2000)

    # 📸 **Primeiro print da seção principal**
    main_sections = page.locator('section.card-highlight-bet.card-highlight-bet-odd-suprema.default').all()
    
    for i, section in enumerate(main_sections):
        section_path = generate_unique_filename(f'main_section_{i+1}')
        section.scroll_into_view_if_needed()
        section.screenshot(path=section_path)
        print(f'📷 Imagem salva: {section_path}')
        
        # Enviar print para o Telegram
        send_image_to_telegram(bot_token, chat_id, topic_id, section_path)

        page.wait_for_timeout(2000)

    # **Lista para armazenar prints**
    saved_images = []

    # 🔍 **Capturar prints de cada container**
    containers = page.locator('div.container.regular').all()
    num_containers = len(containers)

    # Processar até a antepenúltima coluna (excluindo as últimas 3)
    for i, container in enumerate(containers[:num_containers - 3]):  
        print(f'🔄 Clicando no container {i+1} e tirando print...')

        # Garante que está visível
        container.scroll_into_view_if_needed()
        container.click()
        page.wait_for_timeout(3000)  # Aguarda 3s para carregar

        # Captura todas as sections dentro do container
        sections = page.locator('section.card-highlight-bet.card-highlight-bet-odd-suprema.default').all()
        
        for j, section in enumerate(sections):
            section_path = generate_unique_filename(f'container_{i+1}_section_{j+1}')
            section.scroll_into_view_if_needed()
            section.screenshot(path=section_path)
            print(f'📷 Nova imagem salva: {section_path}')
            saved_images.append(section_path)
            
            # Envia a imagem para o Telegram
            send_image_to_telegram(bot_token, chat_id, topic_id, section_path)

            page.wait_for_timeout(2000)

        # Aguarde entre os containers
        page.wait_for_timeout(3000)

    # **Fecha o navegador**
    print("✅ Processo finalizado antes das 3 últimas colunas!")
    browser.close()
