from datetime import datetime
from playwright.sync_api import sync_playwright
import os
import importlib.util
import time

# Função para executar outro arquivo .py com caminho completo ou relativo
def execute_python_file(file_path):
    try:
        # Carrega o módulo dinamicamente
        spec = importlib.util.spec_from_file_location("module_name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"Script {file_path} executado com sucesso.")
    except Exception as e:
        print(f"Erro ao executar o script {file_path}: {e}")

# Função para executar scripts em um intervalo de tempo
def execute_scripts_repeatedly(scripts, interval_minutes, repetitions):
    for _ in range(repetitions):
        for script in scripts:
            execute_python_file(script)
        print(f"Aguardando {interval_minutes} minutos para a próxima execução...")
        time.sleep(interval_minutes * 60)  # Converte minutos para segundos

# Executando vários arquivos .py (com caminho completo ou relativo)
if __name__ == "__main__":
    # BOTS ATIVOS // EXECUÇÃO 24/7
    bots_ativos = [
        r'backend\CalculadoraDutching\dutching.py',
        r'backend\CalculadoraEV\calculadoraEV.py'
    ]

    # CSV DIRETO // EXECUTAR 3 VEZES A CADA 15 MINUTOS
    csv_direto = [
        r'backend\scrapingSportsbooks\Tipo4\tipo4(UXBET).py',
        r'backend\scrapingSportsbooks\Tipo3\tipo3(FAZ1BET).py',
        r'backend\scrapingSportsbooks\Tipo3\tipo3(BETfast).py',
        r'backend\scrapingSportsbooks\Tipo2\apostaTudo.py',
        r'backend\scrapingSportsbooks\Tipo1\BetEsporte.py'
    ]

    # EXECUÇÃO COMPOSTA // EXECUTAR 3 VEZES A CADA 15 MINUTOS
    execucao_composta = [
        (r'backend\scrapingSportsbooks\Tipo1\betPIX365.py', r'backend\convertoresJsonCSV\convertorBETPIX365.py'),
        (r'backend\scrapingSportsbooks\Tipo1\brbet.py', r'backend\convertoresJsonCSV\convertorBRBET.py'),
        (r'backend\scrapingSportsbooks\Tipo1\vaidebet.py', r'backend\convertoresJsonCSV\convertorVAIDEBET.py')
    ]

    # EXECUÇÃO PRINTS // EXECUÇÃO A CADA HORA
    execucao_prints = [
        r'backend\scrapingSportsbooks\Tipo1\ApostaGanha.py'
    ]

    # EXECUÇÃO DO ENVIO DAS APOSTAS QUE ESTÃO NO CSV, A CADA 15 MINUTOS APÓS TODAS EXECUÇÕES ACIMA
    envio_csv = [
        r'backend\envioCSV.py'
    ]

    # Execução dos BOTS ATIVOS (24/7)
    for bot in bots_ativos:
        execute_python_file(bot)

    # Execução dos scripts CSV DIRETO (3 vezes a cada 15 minutos)
    execute_scripts_repeatedly(csv_direto, interval_minutes=15, repetitions=3)

    # Execução dos scripts EXECUÇÃO COMPOSTA (3 vezes a cada 15 minutos)
    for script_pair in execucao_composta:
        for script in script_pair:
            execute_python_file(script)
    execute_scripts_repeatedly([script[0] for script in execucao_composta], interval_minutes=15, repetitions=3)

    # Execução dos scripts EXECUÇÃO PRINTS (a cada hora)
    execute_scripts_repeatedly(execucao_prints, interval_minutes=60, repetitions=1)

    # Execução do script ENVIO CSV (a cada 15 minutos após todas as execuções acima)
    execute_scripts_repeatedly(envio_csv, interval_minutes=15, repetitions=1)