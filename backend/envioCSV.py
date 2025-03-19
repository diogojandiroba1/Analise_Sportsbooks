import csv
import asyncio
from telegram import Bot

# Substitua pelo seu token do Telegram
TOKEN = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'
CHAT_ID = '-1002343785289'  # ID do grupo
TOPIC_ID = 191  # ID do tópico
DELAY = 5  # Atraso entre cada mensagem
INTERVALO_ENVIO = 1200  # 20 minutos em segundos

# Função para carregar apostas já enviadas em um set
def carregar_apostas_enviadas():
    try:
        with open(r"data\\csvS\\apostas_enviadas.csv", mode='r', encoding="utf-8") as file:
            leitor = csv.reader(file)
            # Armazenar as apostas enviadas com base em "casa", "partida" e "aposta", ignorando "odd"
            return {tuple(map(str.strip, row[:3])) for row in leitor}  # Considera apenas as 3 primeiras colunas
    except FileNotFoundError:
        # Se o arquivo não existir, retorna um set vazio
        return set()

# Função para registrar uma nova aposta no arquivo CSV
def registrar_aposta(aposta):
    with open(r"data\\csvS\\apostas_enviadas.csv", mode='a', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(aposta)

# Função para normalizar os dados de apostas no CSV
def normalizar_dados_apostas(arquivo_csv):
    normalizado = []
    
    with open(arquivo_csv, mode='r', encoding='utf-8') as file:
        leitor = csv.reader(file)
        next(leitor)  # Pular cabeçalho
        
        for row in leitor:
            # Normalizar (strip) e fazer ajustes nos campos
            row_normalizada = [campo.strip() for campo in row]

            # Garantir que a "odd" é um valor numérico ou está formatada corretamente
            row_normalizada[3] = row_normalizada[3]  # Aqui você pode fazer mais ajustes, como garantir que seja numérica

            normalizado.append(row_normalizada)
    
    # Retorna os dados normalizados
    return normalizado

# Função assíncrona para enviar apostas
async def enviar_apostas(bot):
    arquivo_csv = r"data\\csvS\\dados_apostas.csv"
    apostas_enviadas = carregar_apostas_enviadas()

    # Normaliza os dados de apostas antes de prosseguir
    apostas_normalizadas = normalizar_dados_apostas(arquivo_csv)

    novas_apostas = False  # Flag para verificar se há novas apostas

    for row in apostas_normalizadas:
        aposta = (
            f"*🏠 Casa:* {row[0]}\n"
            f"*📅 Evento:* {row[1]}\n"
            f"*🎯 Aposta:* {row[2]}\n"
            f"*⚽ Odd:* {row[3]}\n"
            f"*🕒 Data:* {row[4]}\n"
            "\n*🔥 Lembre-se, isso é um alerta de superODD, e não uma tip! BOA SORTE! 🔥*"
        )

        aposta_tuple = tuple(row[:3])  # Normaliza as três primeiras colunas (casa, evento, aposta)

        # Verifica se a aposta já foi enviada, comparando apenas "casa", "evento" e "aposta"
        if aposta_tuple not in apostas_enviadas:
            await bot.send_message(
                chat_id=CHAT_ID,
                text=aposta,
                parse_mode='Markdown',
                message_thread_id=TOPIC_ID
            )
            registrar_aposta(aposta_tuple)  # Registra a aposta como enviada
            apostas_enviadas.add(aposta_tuple)  # Adiciona a aposta ao set
            novas_apostas = True  # Marca que houve ao menos uma aposta enviada
            await asyncio.sleep(DELAY)  # Pequeno atraso entre mensagens

    return novas_apostas  # Retorna se houve novas apostas

# Função principal que executa o envio a cada 20 minutos
async def main():
    bot = Bot(token=TOKEN)

    while True:
        print("🔄 Enviando novas apostas...")

        novas_apostas = await enviar_apostas(bot)

        if novas_apostas:
            print("✔️ Novas apostas enviadas!")
        else:
            print("❌ Nenhuma nova aposta para enviar.")

        print(f"⏳ Aguardando {INTERVALO_ENVIO // 60} minutos para o próximo envio...")
        await asyncio.sleep(INTERVALO_ENVIO)

# Executar o bot
if __name__ == "__main__":
    asyncio.run(main())
