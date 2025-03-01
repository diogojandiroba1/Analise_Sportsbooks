import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
from time import sleep

def apostatudo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  
        page = browser.new_page()
        page.goto('https://apostatudo.bet.br/sports?leagueId=680052790583906304')
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
        iframe_element = page.query_selector('xpath=//*[@id="divPageLayout"]/div[3]/div/div/div/iframe')
        if not iframe_element:
            print("Iframe não encontrado.")
            return
        iframe = iframe_element.content_frame()
        
        # Localizar a div principal com os eventos
        event_container = iframe.query_selector('.eventlist_eu_fe_wrappers_noPadding.components-fe_Tabs_container')
        if not event_container:
            print("Container de eventos não encontrado.")
            return
        
        event_divs = event_container.query_selector_all('div')
        print(f"{len(event_divs)} eventos encontrados.")

        dados = []
        apostas_registradas = set()
        try:
            with open(r'data/CSVs/dados_apostas.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    apostas_registradas.add(tuple(row[1:4]))
        except FileNotFoundError:
            pass
        
        for event_div in event_divs:
            nome_partida_element = event_div.query_selector('.eventlist_eu_fe_LeagueItemMobile_headerName')
            if nome_partida_element:
                nome_partida = nome_partida_element.inner_text().strip()
                print(f"Coletando dados para: {nome_partida}")
                
                aposta_elements = event_div.query_selector_all('.eventlist_eu_fe_OutrightSelection_name')
                odd_elements = event_div.query_selector_all('.eventlist_eu_fe_OutrightSelection_value')
                
                if aposta_elements and odd_elements:
                    for aposta_element, odd_element in zip(aposta_elements, odd_elements):
                        aposta = aposta_element.inner_text().strip()
                        odd = odd_element.inner_text().strip()
                        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        casa_aposta = "ApostaTudo"
                        
                        aposta_tuple = (casa_aposta, nome_partida, aposta, odd, data_hora)
                        aposta_identificador = (nome_partida, aposta, odd)
                        if aposta_identificador not in apostas_registradas:
                            dados.append(aposta_tuple)
                            apostas_registradas.add(aposta_identificador)
                        else:
                            print(f"Aposta já cadastrada: {aposta_tuple}")
                else:
                    print("Nenhuma aposta encontrada para essa partida.")

        if dados:
            with open(r'data/CSVs/dados_apostas.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(dados)
            print(f"{len(dados)} novas apostas adicionadas ao arquivo 'dados_apostas.csv'.")
        else:
            print("Nenhuma aposta nova encontrada.")
        
        input("Pressione Enter para fechar o navegador...")
        browser.close()

apostatudo()