import asyncio
from telegram import Bot

# Substitua pelo seu token do Telegram e chat_id
TOKEN = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'
CHAT_ID = '-1002343785289'  # O ID do grupo (não o nome)

async def listar_topicos():
    bot = Bot(token=TOKEN)
    
    # Obter a lista de tópicos no grupo
    topicos = await bot.get_forum_topics(chat_id=CHAT_ID)
    
    # Exibir os tópicos e seus IDs
    for topico in topicos.topics:
        print(f"Tópico: {topico.name}, ID do Tópico: {topico.message_thread_id}")

# Executar a função
asyncio.run(listar_topicos())