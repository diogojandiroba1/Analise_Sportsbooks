from datetime import datetime
import importlib.util
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("execution_log.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Função para executar um arquivo Python
def execute_python_file(file_path):
    try:
        spec = importlib.util.spec_from_file_location("module_name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        logging.info(f"Script {file_path} executado com sucesso.")
        return True
    except Exception as e:
        logging.error(f"Erro ao executar {file_path}: {e}")
        return False

# Função para executar scripts compostos (scraping + conversão)
def execute_composta(execucao_composta):
    for scraping_script, conversion_script in execucao_composta:
        logging.info(f"Executando scraping: {scraping_script}")
        if execute_python_file(scraping_script):
            logging.info("Aguardando 5 segundos antes da conversão...")
            time.sleep(5)
            logging.info(f"Executando conversão: {conversion_script}")
            execute_python_file(conversion_script)
        else:
            logging.error(f"Falha em {scraping_script}, conversão não será executada.")

# Função para executar scripts com múltiplas threads
def execute_scripts(scripts):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(execute_python_file, script) for script in scripts]
        for future in as_completed(futures):
            future.result()

# Função principal
def main():
    csv_direto = [
        r'backend/scrapingSportsbooks/Tipo4/tipo4(UXBET).py',
        r'backend/scrapingSportsbooks/Tipo3/tipo3(FAZ1BET).py',
        r'backend/scrapingSportsbooks/Tipo3/tipo3(BETfast).py',
        r'backend/scrapingSportsbooks/Tipo1/BetEsporte.py'
    ]

    execucao_composta = [
        (r'backend/scrapingSportsbooks/Tipo1/betPIX365.py', r'backend/convertoresJsonCSV/convertorBETPIX365.py'),
        (r'backend/scrapingSportsbooks/Tipo1/brbet.py', r'backend/convertoresJsonCSV/convertorBRBET.py'),
        (r'backend/scrapingSportsbooks/Tipo1/vaidebet.py', r'backend/convertoresJsonCSV/convertorVAIDEBET.py'),
        (r'backend/convertoresJsonCSV/convertorESTRELABET.py', r'backend/convertoresJsonCSV/convertorESTRELABET.py')
    ]

    while True:
        try:
            # Executar os compostos e CSV direto 3 vezes seguidas
            for _ in range(3):
                logging.info("Executando scripts COMPOSTOS...")
                execute_composta(execucao_composta)
                
                logging.info("Executando scripts CSV DIRETO...")
                execute_scripts(csv_direto)

            logging.info("Aguardando 15 minutos para o próximo ciclo de COMPOSTOS e CSV DIRETO...")
            time.sleep(15 * 60)

        except Exception as e:
            logging.error(f"Erro no loop principal: {e}")
            logging.info("Aguardando 5 minutos antes de reiniciar...")
            time.sleep(300)

if __name__ == "__main__":
    logging.info("Iniciando script principal...")
    main()
