from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

def obter_id_grupo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    print(f"ID do grupo: {chat_id}")

def main():
    token = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'  # Substitua pelo token do seu bot
    updater = Updater(token)

    # Registrar um handler para capturar mensagens e obter o ID do grupo
    updater.dispatcher.add_handler(MessageHandler(Filters.text, obter_id_grupo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()