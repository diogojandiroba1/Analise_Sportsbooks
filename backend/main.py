import threading
import time
import appScrapping
import envioCSV
import asyncio

def start_scraping():
    """Executa o appScrapping normalmente"""
    appScrapping.main()

def start_envio_csv():
    """Aguarda um tempo antes de iniciar o envio de apostas"""
    print("⏳ Aguardando 30 segundos antes de iniciar o envio de apostas...")
    time.sleep(120)  # Espera 30 segundos antes de iniciar
    asyncio.run(envioCSV.main())  # Executa a função assíncrona corretamente

if __name__ == "__main__":
    # Criar threads para rodar os dois scripts ao mesmo tempo
    scraping_thread = threading.Thread(target=start_scraping)
    envio_thread = threading.Thread(target=start_envio_csv)

    # Iniciar o scraping primeiro
    scraping_thread.start()

    # Iniciar o envio CSV após um delay
    envio_thread.start()

    # Esperar ambas as threads terminarem (não acontece pois os loops são infinitos)
    scraping_thread.join()
    envio_thread.join()
