import csv
import asyncio
from telegram import Bot

# Substitua pelo seu token do Telegram
TOKEN = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'
CHAT_ID = '-1002343785289'  # ID do grupo
TOPIC_ID = 191  # ID do tópico
DELAY = 4  # Atraso entre cada mensagem
INTERVALO_ENVIO = 1200  # 20 minutos em segundos

# Função para carregar apostas já enviadas em um set
def carregar_apostas_enviadas():
    try:
        with open("data\\csvS\\apostas_enviadas.csv", mode='r', encoding="utf-8") as file:
            leitor = csv.reader(file)
            # Armazenar as apostas enviadas como tuplas
            return {tuple(row) for row in leitor}
    except FileNotFoundError:
        # Se o arquivo não existir, retorna um set vazio
        return set()

# Função para registrar uma nova aposta no arquivo CSV
def registrar_aposta(aposta):
    with open("data\\csvS\\apostas_enviadas.csv", mode='a', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(aposta)

# Função assíncrona para enviar apostas
async def enviar_apostas(bot):
    arquivo_csv = "data\\csvS\\dados_apostas.csv"
    apostas_enviadas = carregar_apostas_enviadas()

    novas_apostas = False  # Flag para verificar se há novas apostas

    with open(arquivo_csv, mode='r', encoding='utf-8') as file:
        leitor = csv.reader(file)
        next(leitor)  # Pular cabeçalho

        for row in leitor:
            aposta = (
                f"*🏠 Casa:* {row[0]}\n"
                f"*📅 Evento:* {row[1]}\n"
                f"*🎯 Aposta:* {row[2]}\n"
                f"*⚽ Odd:* {row[3]}\n"
                f"*🕒 Data:* {row[4]}\n"
                "\n*🔥 Boa sorte e aproveite as apostas! 🔥*"
            )

            aposta_tuple = tuple(row)  # Converte a linha para uma tupla para verificação

            # Verifica se a aposta já foi enviada
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
