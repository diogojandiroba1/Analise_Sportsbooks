import cloudscraper
import json
from time import sleep

# Criar o scraper que imita um navegador
scraper = cloudscraper.create_scraper()

# URL da API
url = "https://sb2frontend-altenar2.biahosted.com/api/widget/GetOutrightEvents?culture=pt-BR&timezoneOffset=180&integration=estrelabet&deviceType=1&numFormat=en-GB&countryCode=BR&eventCount=0&sportId=0&catIds=1325"


# Caminho do arquivo JSON onde os dados serão salvos
caminho_arquivo = "data/dataESTRELABET.json"

while True:
    try:
        # Fazer a requisição usando cloudscraper
        response = scraper.get(url)
        response.raise_for_status()  # Levanta um erro se o status não for 200
        
        # Converter resposta para JSON
        dados_json = response.json()
        print("✅ Dados obtidos com sucesso!")

        # Salvar os dados no arquivo
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)
            print("💾 Dados salvos!")

    except cloudscraper.exceptions.CloudflareChallengeError as e:
        print(f"⚠️ Cloudflare bloqueou a requisição: {e}")

    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

    # Esperar 60 segundos antes da próxima requisição
    sleep(60)
