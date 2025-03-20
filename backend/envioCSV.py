import csv
import asyncio
import re
from telegram import Bot

# Substitua pelo seu token do Telegram
TOKEN = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'
CHAT_ID = '-1002647595950'  # ID do grupo
TOPIC_ID = 963  # ID do tópico
DELAY = 5  # Atraso entre cada mensagem
INTERVALO_ENVIO = 60  # 20 minutos em segundos

# Função para escapar caracteres especiais no Markdown

def escape_markdown(text):
    """Escapa caracteres especiais para evitar erros no MarkdownV2"""
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)

# Função para carregar apostas já enviadas em um set
def carregar_apostas_enviadas():
    try:
        with open(r"data/csvS/apostas_enviadas.csv", mode='r', encoding="utf-8") as file:
            leitor = csv.reader(file)
            return {tuple(map(str.strip, row[:3])) for row in leitor}  # Considera apenas as 3 primeiras colunas
    except FileNotFoundError:
        return set()

# Função para registrar uma nova aposta no arquivo CSV
def registrar_aposta(aposta):
    with open(r"data/csvS/apostas_enviadas.csv", mode='a', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(aposta)

# Função para normalizar os dados de apostas no CSV
def normalizar_dados_apostas(arquivo_csv):
    normalizado = []
    with open(arquivo_csv, mode='r', encoding='utf-8') as file:
        leitor = csv.reader(file)
        next(leitor)  # Pular cabeçalho
        for row in leitor:
            row_normalizada = [campo.strip() for campo in row]
            normalizado.append(row_normalizada)
    return normalizado

# Função assíncrona para enviar apostas
async def enviar_apostas(bot):
    arquivo_csv = r"data/csvS/dados_apostas.csv"
    apostas_enviadas = carregar_apostas_enviadas()
    apostas_normalizadas = normalizar_dados_apostas(arquivo_csv)
    novas_apostas = False

    for row in apostas_normalizadas:
        aposta = (
            f"*🏠 Casa:* {escape_markdown(row[0])}\n"
            f"*📅 Evento:* {escape_markdown(row[1])}\n"
            f"*🎯 Aposta:* {escape_markdown(row[2])}\n"
            f"*⚽ Odd:* {escape_markdown(row[3])}\n"
            f"*🕒 Data:* {escape_markdown(row[4])}\n"
            f"*🚧 Limite: r$* \n"
            f"*🔗 Link:* {escape_markdown(row[5])}\n"
            "\n🔥 Lembre\-se ** isso é um alerta de superODD e não uma tip** BOA SORTE 🔥"
        )

        aposta_tuple = tuple(row[:3])
        if aposta_tuple not in apostas_enviadas:
            await bot.send_message(
                chat_id=CHAT_ID,
                text=aposta,
                parse_mode='MarkdownV2',
                message_thread_id=TOPIC_ID
            )
            registrar_aposta(aposta_tuple)
            apostas_enviadas.add(aposta_tuple)
            novas_apostas = True
            await asyncio.sleep(DELAY)
    return novas_apostas

# Função principal
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

if __name__ == "__main__":
    asyncio.run(main())