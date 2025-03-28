import os
import time
import csv
import cv2
import pytesseract
import re
from playwright.sync_api import sync_playwright

# Função para extrair dados da imagem usando pytesseract
def extract_data_from_image(image_path):
    image = cv2.imread(image_path)

    # Converter para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Passar a imagem processada para o Tesseract
    text = pytesseract.image_to_string(gray, lang='por', config='--psm 6')
    print("Texto extraído:\n", text)

    # Dividir o texto em linhas
    lines = text.splitlines()

    # Inicializar variáveis para armazenar as informações
    partida = ""
    aposta = ""
    odd = ""

    # Garantir que a partida será sempre a segunda linha
    if len(lines) > 1:
        partida = lines[1].strip()  # A partida está sempre na segunda linha

    # Flag para identificar quando estamos entre a partida e a odd
    capturando_aposta = False

    # Iterar pelas linhas para capturar as apostas e odds
    for i, line in enumerate(lines[2:]):  # Começar da terceira linha (após a partida)
        line = line.strip()  # Remover espaços extras
        
        # Capturar a odd após o ">" ou "»"
        if '>' in line or '»' in line:
            # Expressão regular para pegar o número imediatamente após ">" ou "»"
            odd_match = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*$', line)
            if odd_match:
                odd = odd_match.group(1)  # Pega o número após o símbolo
            continue  # Passar para a próxima linha

        # Se estamos entre a partida e a odd, capturar a aposta
        if line:
            aposta += line + " "  # Adicionar a linha à aposta, separada por espaço

    # Exibir os resultados
    print(f"Partida: {partida}")
    print(f"Aposta: {aposta.strip()}")  # Remover espaços extras no final
    print(f"Odd: {odd}")

    return partida, aposta.strip(), odd


# Função para salvar os dados no CSV
def save_to_csv(casa, evento, aposta, odd, data, link, csv_file):
    # Verificar se a aposta + odd já existe
    if not check_duplicate_in_csv(aposta, odd, csv_file):
        with open(csv_file, 'a', newline='', encoding='utf-8') as file:  # Adicione encoding='utf-8'
            writer = csv.writer(file)
            writer.writerow([casa, evento, aposta, odd, data, link])
            print(f"✅ Dados da aposta '{aposta}' com odd '{odd}' salvos no CSV.")
    else:
        print(f"⚠️ Aposta '{aposta}' com odd '{odd}' já está no CSV. Ignorando.")

# Função para verificar se a aposta já existe no CSV
def check_duplicate_in_csv(aposta, odd, csv_file):
    if not os.path.exists(csv_file):
        return False  # Se o arquivo não existir, não há duplicatas

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:  # Adicione encoding='utf-8'
        reader = csv.reader(file)
        for row in reader:
            # Verificar se a combinação aposta + odd já existe no CSV
            if row[2] == aposta and row[3] == odd:
                return True
    return False


# Configurações
url = "https://www.bet365.bet.br/"
output_folder = "prints"
os.makedirs(output_folder, exist_ok=True)

# Caminho para o CSV onde os dados serão armazenados
csv_file = r'data\\csvS\\dados_apostas.csv'

if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:  # Adicione encoding='utf-8'
        writer = csv.writer(file)
        writer.writerow(["Casa", "Evento", "Aposta", "Odd", "Data", "Link"])

brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"        
# Processamento da página e captura de imagem
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,  # headless=False para ver o navegador
        executable_path=brave_path,  # Define o Brave como navegador
        args=["--no-sandbox"]
    )
    page = browser.new_page()
    # Acessa a URL
    page.goto('https://www.bet365.bet.br/#/HO/')
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

            # Extrair dados da imagem
            partida, aposta, odd = extract_data_from_image(screenshot_path)

            # Salvar no CSV se não for duplicado
            save_to_csv("BET365", partida, aposta, odd, time.strftime("%Y-%m-%d %H:%M:%S"), "https://www.bet365.bet.br/", csv_file)

            time.sleep(2)  # Pequena pausa entre capturas

    # Captura os Boosts do Popular Bet Content
    images2 = page.query_selector_all('.pbb-PopularBet_Content .pbb-PopularBet_BoostLogo.pbb-SuperBetBoost')
    print(f"🔍 Encontradas {len(images2)} imagens de Super BetBoost para capturar.")

    for i, img in enumerate(images2, start=1):
        parent_div = img.evaluate_handle("(el) => el.closest('.pbb-PopularBet_Content')")
        if parent_div:
            screenshot_path = os.path.join(output_folder, f"super_bet_boost_{i}.png")
            parent_div.screenshot(path=screenshot_path)
            print(f"📸 Print salvo: {screenshot_path}")

            # Extrair dados da imagem
            partida, aposta, odd = extract_data_from_image(screenshot_path)

            # Salvar no CSV se não for duplicado
            save_to_csv("BET365", partida, aposta, odd, time.strftime("%Y-%m-%d %H:%M:%S"), "https://www.bet365.bet.br/", csv_file)

            time.sleep(2)  # Pequena pausa entre capturas

    browser.close()
    print("✅ Processo concluído!")
