import os
import pandas as pd
from telegram import Update
from telegram.ext import Application, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # Importar o agendador

# Função para ler o arquivo CSV e formatar as apostas
def ler_apostas(csv_file):
    df = pd.read_csv(csv_file, header=None, names=["Casa", "Evento", "Aposta", "Odd", "Data"])
    apostas_formatadas = []
    for _, row in df.iterrows():
        aposta_formatada = (
            f"🏟️ **Evento**: {row['Evento']}\n"
            f"🎲 **Aposta**: {row['Aposta']}\n"
            f"💰 **Odd**: {row['Odd']}\n"
            f"📅 **Data**: {row['Data']}\n"
            f"-----------------------------"
        )
        apostas_formatadas.append(aposta_formatada)
    return "\n".join(apostas_formatadas)

# Função para enviar as apostas no grupo
async def enviar_apostas_no_grupo(context: ContextTypes.DEFAULT_TYPE):
    csv_file = 'data\\csvS\\dados_apostas.csv'  # Caminho do arquivo CSV
    apostas = ler_apostas(csv_file)
    chat_id = -1002343785289  # ID do grupo
    await context.bot.send_message(chat_id=chat_id, text=f"📊 **Apostas do Dia**\n\n{apostas}")

# Função principal para iniciar o bot
async def main():
    token = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'  # Token do bot

    # Criar a aplicação do bot
    application = Application.builder().token(token).build()

    # Criar o agendador
    scheduler = AsyncIOScheduler()

    # Agendar o envio de apostas (por exemplo, a cada 1 hora)
    scheduler.add_job(
        enviar_apostas_no_grupo, 
        'interval', 
        seconds=3600,  # Intervalo de 1 hora
        args=[application], 
        id='enviar_apostas'
    )
    scheduler.start()

    # Iniciar o bot com o loop de eventos
    await application.run_polling()

# Ajuste para ambientes com loop de eventos já rodando
if __name__ == '__main__':
    import asyncio

    try:
        # Tente rodar a função principal
        asyncio.run(main())
    except RuntimeError:
        # Caso o erro de loop de eventos já rodando ocorra, execute a função sem o asyncio.run
        print("Loop de eventos já está rodando. Usando o loop atual.")
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
