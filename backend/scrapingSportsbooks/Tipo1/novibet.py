import csv
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

def configurar_navegador():
    """Inicializa o navegador e retorna a página carregada."""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://www.novibet.bet.br/apostas-esportivas/enhanced-odds/4796050/competitions?ids=6174719,6233313,6247087')
    return p, browser, page

def fechar_popup_inicial(page):
    """Fecha os pop-ups iniciais da página."""
    page.click('//*[@id="cdk-dialog-0"]/app-age-restriction/div/div/app-age-restriction-options/div/div[1]/cm-checkbox/div/div[1]/span')
    page.wait_for_timeout(2000)
    page.click('//*[@id="cdk-dialog-0"]/app-age-restriction/div/div/nds-button/button/span')
    page.wait_for_timeout(3000)
    page.click('//*[@id="cdk-overlay-1"]/app-dialog/app-register-or-login/div/div[1]/cm-icon')
    page.wait_for_timeout(2000)

def carregar_apostas_existentes(arquivo_csv):
    """Carrega apostas existentes no CSV para evitar duplicação."""
    apostas_registradas = set()
    if os.path.exists(arquivo_csv):
        with open(arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Pular cabeçalho
            for row in reader:
                apostas_registradas.add(tuple(row[:4]))
    else:
        with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Casa', 'Evento', 'Aposta', 'Odd', 'Data'])
    return apostas_registradas

def coletar_apostas(page, apostas_registradas, dados):
    """Coleta as apostas disponíveis na página ignorando a primeira partida."""
    page.wait_for_selector("cm-card-title.no-ellipsis", timeout=10000)
    
    partidas = page.query_selector_all("div.couponSelections_subItem")
    print(f"Encontradas {len(partidas)} partidas.")
    
    # Ignorar a primeira partida
    partidas = partidas[1:] if len(partidas) > 1 else []

    for partida in partidas:
        partida_texto = partida.query_selector("cm-card-title.no-ellipsis")
        if not partida_texto:
            continue
        
        partida_texto = partida_texto.inner_text().strip()
        apostas = partida.query_selector_all("cm-card.competitionEventMarketview")
        
        for aposta in apostas:
            aposta_texto = aposta.query_selector("span.marketBetItem_caption")
            odd_texto = aposta.query_selector("div.marketBetItem_price.enhanced")
            
            if aposta_texto and odd_texto:
                aposta_texto = aposta_texto.inner_text().strip()
                odd_texto = odd_texto.inner_text().strip()
                
                aposta_identificador = ("Novibet", partida_texto, aposta_texto, odd_texto)
                if aposta_identificador not in apostas_registradas:
                    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    dados.append((*aposta_identificador, data_hora))
                    apostas_registradas.add(aposta_identificador)

def navegar_pelos_esportes(page):
    """Navega pelos esportes para coletar mais apostas."""
    esportes = page.query_selector_all("div.couponHeaderMultiple_leagueTitleMultiple")
    print(f"Encontrados {len(esportes)} esportes.")

    esportes = esportes[1:] if len(esportes) > 1 else []

    for esporte in esportes:
        esporte.click()
        page.wait_for_timeout(5000)  # Tempo para carregar as novas apostas

def salvar_dados_csv(arquivo_csv, dados):
    """Salva os dados coletados no arquivo CSV."""
    if dados:
        with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(dados)
        print(f"{len(dados)} novas apostas adicionadas ao arquivo '{arquivo_csv}'.")
    else:
        print("Nenhuma aposta nova encontrada.")

def novibet():
    """Fluxo principal para coleta de apostas."""
    p, browser, page = configurar_navegador()
    fechar_popup_inicial(page)
    arquivo_csv = r'data/csvS/dados_apostas.csv'
    apostas_registradas = carregar_apostas_existentes(arquivo_csv)
    dados = []
    
    coletar_apostas(page, apostas_registradas, dados)
    navegar_pelos_esportes(page)
    coletar_apostas(page, apostas_registradas, dados)
    
    salvar_dados_csv(arquivo_csv, dados)
    browser.close()
    p.stop()

# Executa a função
novibet()
