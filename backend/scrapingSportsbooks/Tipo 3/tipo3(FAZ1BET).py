import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
from time import sleep

# Função principal
def faz1bet():
    with sync_playwright() as p:
        # Inicia o navegador
        browser = p.chromium.launch(headless=False)  # headless=False para ver o navegador
        page = browser.new_page()

        # Acessa a URL
        page.goto('https://faz1.bet.br/br/sportsbook/prematch#/prematch/selection/197')

        # Aguarda o carregamento da página
        page.wait_for_selector('body')

        # Localiza o iframe
        iframe = page.query_selector('xpath=/html/body/main/iframe')

        if iframe:
            print("Iframe encontrado!")
            # Muda o contexto para o iframe
            iframe_content = iframe.content_frame()

            # Localiza a div com o XPath especificado
            div_alvo = iframe_content.query_selector('xpath=//*[@id="prematch"]/div[2]/div[1]/div')

            if div_alvo:
                print("Div alvo encontrada dentro do iframe!")
                # Encontra todas as divs com a classe "match-list" ou "match-list is-mobile"
                divs_match_list = div_alvo.query_selector_all('div.match-list, div.match-list.is-mobile')
                quantidade_divs = len(divs_match_list)
                print(f"Quantidade de divs com classe 'match-list' ou 'match-list is-mobile': {quantidade_divs}")

                # Lista para armazenar os dados extraídos
                dados = []
                apostas_registradas = set()  # Usando um set para armazenar combinações únicas (partida, aposta, odd)

                # Tenta abrir o arquivo CSV para leitura, para verificar apostas já registradas
                try:
                    with open('data/CSVs/dados_apostas.csv', mode='r', newline='') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            # Adiciona a combinação (partida, aposta, odd) ao set
                            apostas_registradas.add(tuple(row[1:4]))  # Combinação (partida, aposta, odd)
                except FileNotFoundError:
                    pass  # Se o arquivo não existir, criamos um novo mais tarde

                # Itera sobre as divs
                for i, div in enumerate(divs_match_list):
                    print(f"Processando div {i + 1}...")
                    # Localiza o <li> com a classe "outright-row" dentro da div atual
                    li_outright_row = div.query_selector('li.outright-row')
                    if li_outright_row:
                        print(f"Clicando no <li> da div {i + 1}...")
                        li_outright_row.click()
                        sleep(1)  # Espera 1 segundo entre os cliques (ajuste conforme necessário)
                        
                        # Extração de dados após o clique
                        casa_aposta = "Faz1Bet"  # Fixo
                        partida = div.query_selector('p.dotted-hidden.team-name').inner_text().strip() if div.query_selector('p.dotted-hidden.team-name') else "N/A"
                        aposta = div.query_selector('div.title').inner_text().strip() if div.query_selector('div.title') else "N/A"

                        # Pega a odd da aposta
                        odds = div.query_selector_all('span:nth-child(2)')  # Pega todas as odds da aposta
                        odds_text = [odd.inner_text().strip() for odd in odds if odd.inner_text().strip()]

                        # Data e hora atual
                        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Verificação de duplicatas e adição dos dados
                        for odd in odds_text:
                            aposta_tuple = (casa_aposta, partida, aposta, odd, data_hora)
                            aposta_identificador = (partida, aposta, odd)  # Combinação única para verificar duplicatas
                            if aposta_identificador not in apostas_registradas:
                                dados.append(aposta_tuple)  # Adiciona os dados ao conjunto
                                apostas_registradas.add(aposta_identificador)  # Marca como registrada
                            else:
                                print(f"Aposta já cadastrada: {aposta_tuple}")

            else:
                print("Div alvo NÃO encontrada dentro do iframe.")
        else:
            print("Iframe NÃO encontrado.")

        # Adiciona os dados no arquivo CSV sem escrever o cabeçalho
        if dados:
            with open('data/CSVs/dados_apostas.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(dados)  # Adiciona os dados extraídos

            print(f"{len(dados)} dados adicionados ao arquivo 'dados_apostas.csv'.")
        else:
            print("Nenhuma aposta nova encontrada.")

        # Mantém o navegador aberto até que o usuário pressione Enter
        input("Pressione Enter para fechar o navegador...")

        # Fecha o navegador
        browser.close()

# Executa a função
faz1bet()
