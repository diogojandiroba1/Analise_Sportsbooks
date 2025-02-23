import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime
import os

async def betesporte_riscoZero(page):
    dados2 = []
    url_riscoZero = 'https://betesporte.bet.br/sports/desktop/sport-league/999/4200000006'
    await page.goto(url_riscoZero)
    
    try:
        await page.wait_for_selector('//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[2]/div/div[2]', timeout=5000)
        aposta_riscoZero = await page.query_selector_all('//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[2]/div/div[2]')
        
        if aposta_riscoZero:  # Se encontrar apostas de riscoZero
            odds_elements = await page.query_selector_all('//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[4]/div/app-odd/div/div')
            for index, element in enumerate(odds_elements, start=1):
                aposta_text = await aposta_riscoZero[index-1].text_content()
                odd_text = await element.text_content()
                print(f'Odd Risco Zero: {odd_text} para {aposta_text}')
                dados2.append(['BETESPORTE', 'risco0', aposta_text, odd_text])
    except:
        print("Não encontrou apostas de Risco Zero.")
    
    return dados2

async def betesporte_superOdd(page):
    dados1 = []
    url_super_odd = "https://betesporte.bet.br/sports/desktop/sport-league/999/4200000001"
    await page.goto(url_super_odd)
    
    await page.wait_for_selector('//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[2]/div/div[2]', timeout=5000)
    aposta_superOdd = await page.query_selector_all('//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[2]/div/div[2]')
    odds_elements = await page.query_selector_all('//*[@id="bets"]/app-sport-league-desktop/div/div[3]/app-new-event-list-pre/section/div/div[2]/div[4]/div/app-odd/div/div')
    
    for index, element in enumerate(odds_elements, start=1):
        aposta_text = await aposta_superOdd[index-1].text_content()
        odd_text = await element.text_content()
        print(f'Super Odd: {odd_text} para {aposta_text}')
        dados1.append(['BETESPORTE', 'SUPERodd', aposta_text, odd_text])

    return dados1

async def salvar_dados(dados):
    try:
        df_existente = pd.read_csv(r'data\dados_apostas.csv')
    except FileNotFoundError:
        df_existente = pd.DataFrame(columns=['Casa de Apostas', 'Partida', 'Aposta', 'Odd', 'Data de Adição'])

    df_novo = pd.DataFrame(dados, columns=['Casa de Apostas', 'Partida', 'Aposta', 'Odd'])

    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df_novo['Data de Adição'] = data_atual

    # Verifica duplicatas e remove
    df_novo = df_novo[~df_novo.apply(lambda row: ((df_existente['Casa de Apostas'] == row['Casa de Apostas']) &
                                                   (df_existente['Partida'] == row['Partida']) &
                                                   (df_existente['Aposta'] == row['Aposta'])).any(), axis=1)]

    df_completo = pd.concat([df_existente, df_novo], ignore_index=True)
    df_completo.to_csv(r'data\dados_apostas.csv', index=False)
    print("Dados salvos no arquivo 'dados_apostas.csv'")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headless=True se não quiser ver o navegador
        page1 = await browser.new_page()  # Primeira aba para Risco Zero
        page2 = await browser.new_page()  # Segunda aba para Super Odd

        try:
            while True:
                # Executa a busca em ambas as abas simultaneamente
                dados1, dados2 = await asyncio.gather(
                    betesporte_riscoZero(page1),  # Busca na primeira aba
                    betesporte_superOdd(page2)    # Busca na segunda aba
                )

                # Combina os dados e salva
                dados = dados1 + dados2
                await salvar_dados(dados)
                await asyncio.sleep(30)

        except Exception as e:
            print(f"Erro ao acessar a página ou localizar o elemento: {e}")

        finally:
            await browser.close()

# Executa o programa
asyncio.run(main())
