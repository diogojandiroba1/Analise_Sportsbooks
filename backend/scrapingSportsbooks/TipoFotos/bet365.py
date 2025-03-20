import os
import requests
import time
from playwright.sync_api import sync_playwright

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

# Configurações
url = "https://www.bet365.bet.br/"
bot_token = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'  # Substitua pelo seu token do bot
chat_id = '-1002647595950'  # Substitua pelo ID do grupo
topic_id = 186  # ID do tópico correto
output_folder = "prints"
os.makedirs(output_folder, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    page = context.new_page()
    page.goto(url, timeout=60000)
    
    # Esperar botão de cookies
    try:
        page.locator('xpath=/html/body/div[3]/div/div[2]/div[3]').wait_for(timeout=20000)
        page.click('xpath=/html/body/div[3]/div/div[2]/div[3]')
        print("✅ Cookies aceitos")
    except:
        print("⚠️ Botão de cookies não encontrado, seguindo adiante...")

    # Esperar carregamento do conteúdo
    page.wait_for_selector('.pbb-PopularBetBuilder_BoostLogo.pbb-BetBoost', timeout=30000)

    # Captura os Boosts do Popular Bet Builder
    images1 = page.query_selector_all('.pbb-PopularBetBuilder_BoostLogo.pbb-BetBoost')
    print(f"🔍 Encontradas {len(images1)} imagens de BetBoost para capturar.")

    for i, img in enumerate(images1, start=1):
        parent_div = img.evaluate_handle("(el) => el.closest('.pbb-PopularBetBuilder.gl-Participant_General')")
        if parent_div:
            screenshot_path = os.path.join(output_folder, f"bet_boost_{i}.png")
            parent_div.screenshot(path=screenshot_path)
            print(f"📸 Print salvo: {screenshot_path}")
            send_image_to_telegram(bot_token, chat_id, topic_id, screenshot_path)
            time.sleep(2)  # Pequena pausa entre envios

    # Captura os Boosts do Popular Bet Content
    images2 = page.query_selector_all('.pbb-PopularBet_Content .pbb-PopularBet_BoostLogo.pbb-SuperBetBoost')
    print(f"🔍 Encontradas {len(images2)} imagens de Super BetBoost para capturar.")

    for i, img in enumerate(images2, start=1):
        parent_div = img.evaluate_handle("(el) => el.closest('.pbb-PopularBet_Content')")
        if parent_div:
            screenshot_path = os.path.join(output_folder, f"super_bet_boost_{i}.png")
            parent_div.screenshot(path=screenshot_path)
            print(f"📸 Print salvo: {screenshot_path}")
            send_image_to_telegram(bot_token, chat_id, topic_id, screenshot_path)
            time.sleep(2)  # Pequena pausa entre envios

    browser.close()
    print("✅ Processo concluído!")
