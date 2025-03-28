import threading
import time
import appScrapping
import envioCSV 
import asyncio
import importlib.util
import logging

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    p.chromium.launch()  # Não precisa chamar install() explicitamente



# Lista de arquivos do TipoFotos para executar uma vez por dia
tipo_fotos_scripts = [
    "backend/scrapingSportsbooks/TipoFotos/ApostaGanha.py",
    "backend/scrapingSportsbooks/TipoFotos/EsportivaBet.py"
]

def execute_python_file(file_path):
    """Executa um arquivo Python a partir do caminho fornecido"""
    try:
        spec = importlib.util.spec_from_file_location("module_name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        logging.info(f"✅ Script {file_path} executado com sucesso.")
    except Exception as e:
        logging.error(f"❌ Erro ao executar {file_path}: {e}")

def start_scraping():
    """Executa o appScrapping normalmente"""
    appScrapping.main()

def start_tipo_fotos():
    """Executa os scripts de TipoFotos uma vez por dia"""
    while True:
        logging.info("📸 Executando scripts do TipoFotos...")
        for script in tipo_fotos_scripts:
            execute_python_file(script)
        
        logging.info("⏳ Aguardando 24 horas antes da próxima execução de TipoFotos...")
        time.sleep(3 * 60 * 60)  # Aguarda 24 horas

def start_envio_csv():
    """Aguarda um tempo antes de iniciar o envio de apostas"""
    logging.info("⏳ Aguardando 30 segundos antes de iniciar o envio de apostas...")
    time.sleep(30)  # Espera 120 segundos antes de iniciar
    asyncio.run(envioCSV.main())  # Executa a função assíncrona corretamente

if __name__ == "__main__":
    # Criar threads para rodar os scripts simultaneamente
    scraping_thread = threading.Thread(target=start_scraping, daemon=True)
    tipo_fotos_thread = threading.Thread(target=start_tipo_fotos, daemon=True)
    envio_thread = threading.Thread(target=start_envio_csv, daemon=True)

    # Iniciar as threads
    scraping_thread.start()
    tipo_fotos_thread.start()

    # Esperar 10 segundos para os scrapers rodarem antes de iniciar o envio
    time.sleep(10)
    envio_thread.start()

    # Manter o programa rodando
    scraping_thread.join()
    tipo_fotos_thread.join()
    envio_thread.join()
