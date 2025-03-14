import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler

# Token do seu bot (fornecido pelo BotFather)
TELEGRAM_API_TOKEN = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'

# Link gerado pelo Stripe para pagamento
STRIPE_PAYMENT_LINK = 'https://buy.stripe.com/test_8wM2c2fB051VfW85kk'

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Função de iniciar o bot
async def start(update, context):
    await update.message.reply_text(
        "Olá! Para acessar o grupo pago, faça um pagamento clicando abaixo:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Pagar agora", url=STRIPE_PAYMENT_LINK)
        ]])
    )

# Função para quando o usuário clicar no botão (sem necessidade de callback)
async def payment(update, context):
    await update.message.reply_text(
        "Você será redirecionado para o Stripe para realizar o pagamento."
    )

# Função para configurar e iniciar o bot
def main():
    # Criar uma aplicação
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Adicionar manipuladores de comandos
    application.add_handler(CommandHandler("start", start))

    # Iniciar o bot
    application.run_polling()

if __name__ == '__main__':
    main()
