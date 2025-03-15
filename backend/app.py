import csv
import asyncio
from telegram import Bot

# Substitua pelo seu token do Telegram
TOKEN = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'
CHAT_ID = '-1002343785289'  # ID do grupo
TOPIC_ID = 191  # ID do tópico
DELAY = 2  # Atraso em segundos entre cada envio de mensagem

# Função para carregar apostas já enviadas em um set
def carregar_apostas_enviadas():
    try:
        with open("data\\csvS\\apostas_enviadas.csv", mode='r', encoding="utf-8") as file:
            leitor = csv.reader(file)
            # Retorna um set com todas as apostas já enviadas
            return {tuple(row) for row in leitor}
    except FileNotFoundError:
        # Se o arquivo não existir, retorna um set vazio
        return set()

# Função para registrar uma nova aposta no arquivo CSV
def registrar_aposta(aposta):
    with open("data\\csvS\\apostas_enviadas.csv", mode='a', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(aposta)

# Função assíncrona para enviar cada linha do CSV
async def enviar_apostas():
    arquivo_csv = "data\\csvS\\dados_apostas.csv"  # Caminho do arquivo original com as apostas

    # Crie uma instância do bot
    bot = Bot(token=TOKEN)

    # Carregar apostas já enviadas
    apostas_enviadas = carregar_apostas_enviadas()

    # Abrir o arquivo CSV com as apostas
    with open(arquivo_csv, mode='r', encoding='utf-8') as file:
        leitor = csv.reader(file)

        # Pular o cabeçalho se existir
        next(leitor)

        # Enviar cada linha do CSV como mensagem
        for row in leitor:
            aposta = (
                f"*🏠 Casa:* {str(row[0])}\n"
                f"*📅 Evento:* {str(row[1])}\n"
                f"*🎯 Aposta:* {str(row[2])}\n"
                f"*⚽ Odd:* {str(row[3])}\n"
                f"*🕒 Data:* {str(row[4])}\n"
                "\n*🔥 Boa sorte e aproveite as apostas! 🔥*"
            )

            # Verificar se a aposta já foi enviada
            aposta_tuple = tuple(row)  # Converte a linha em uma tupla para comparação
            if aposta_tuple not in apostas_enviadas:
                # Enviar a mensagem para o Telegram no tópico específico
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=aposta,
                    parse_mode='Markdown',
                    message_thread_id=TOPIC_ID  # Especifica o ID do tópico
                )
                # Registrar a aposta como enviada
                registrar_aposta(aposta_tuple)
                # Adicionar a aposta ao set de apostas enviadas
                apostas_enviadas.add(aposta_tuple)

                # Adicionar um atraso entre cada envio
                await asyncio.sleep(DELAY)
            else:
                print(f"Aposta já enviada: {aposta}")

# Função principal para executar o envio de apostas
async def main():
    await enviar_apostas()

# Rodar o bot com asyncio
if __name__ == "__main__":
    asyncio.run(main())