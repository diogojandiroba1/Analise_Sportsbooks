import csv
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

def extrair_apostas(page):
    dados = []
    apostas_registradas = set()
    arquivo_csv = r'data\csvS\dados_apostas.csv'

    # Carregar apostas já registradas
    if os.path.exists(arquivo_csv):
        with open(arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Pular cabeçalho
            for row in reader:
                apostas_registradas.add(tuple(row[:4]))
    
    # Aguardar apostas carregarem
    try:
        page.wait_for_selector("div.EventBoxstyled__EventBoxContainerBase-sc-ksk2ut-32", timeout=5000)
    except:
        print("Nenhuma aposta encontrada nesta página.")
        return

    # Localizar todas as apostas
    apostas = page.query_selector_all("div.EventBoxstyled__EventBoxContainerBase-sc-ksk2ut-32")
    
    for aposta in apostas:
        try:
            evento = aposta.query_selector("div.OutrightEventBoxVariant0styled__OutrightEventName-sc-1e7nfsf-2").inner_text()
            aposta_nome = aposta.query_selector("span.OddBoxVariant0styled__OddLabel-sc-1ypym0p-1").inner_text()
            odd = aposta.query_selector("div.OddBoxVariant0styled__OddValue-sc-1ypym0p-6").inner_text()
            casa = "McGames"
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if (casa, evento, aposta_nome, odd) not in apostas_registradas:
                dados.append([casa, evento, aposta_nome, odd, data])
        except AttributeError:
            continue  # Caso algum elemento não seja encontrado, evita erro

    # Salvar novas apostas no CSV
    if dados:
        with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(dados)
        print(f"{len(dados)} novas apostas adicionadas ao arquivo 'dados_apostas.csv'.")
    else:
        print("Nenhuma aposta nova encontrada.")

def mcgames():
    urls = [
        "https://mcgames.bet.br/sports#/sport/115/category/1365/championship/50459",
        "https://mcgames.bet.br/sports#/sport/90/category/1325/championship/51072"
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for i, url in enumerate(urls):
            page.goto(url)
            page.wait_for_load_state("networkidle")  # Esperar a página carregar completamente
            
            # Clicar no botão de verificação apenas na primeira página
            if i == 0:
                try:
                    page.locator("xpath=/html/body/div[5]/div[1]/div[2]/div[2]/button[2]").click()
                    page.wait_for_timeout(10000)  # Pequeno delay para garantir o carregamento
                except:
                    pass
            
            extrair_apostas(page)

        browser.close()

if __name__ == "__main__":
    mcgames()
