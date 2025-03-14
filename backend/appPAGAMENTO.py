import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import requests

# 🔑 Substitua com seu TOKEN do BotFather
TELEGRAM_API_TOKEN = '7980433701:AAFeSQ5J2tCVdNDKfwwEjImx5NF2MIaK6zQ'

# 🔗 Substitua pelo seu link de pagamento gerado no Yampi
YAMPI_PAYMENT_LINK = 'https://elite-das-bets.pay.yampi.com.br/r/KCXPZZ45WL'

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Dicionário para armazenar usuários pagos (simulação, use um banco de dados em produção)
usuarios_pagos = {}

# Função de iniciar o bot
async def start(update, context):
    await update.message.reply_text(
        "Olá! Para acessar o grupo pago, clique no botão abaixo e faça o pagamento:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("💳 Pagar agora", url=YAMPI_PAYMENT_LINK)
        ]])
    )

# Função para verificar pagamento manualmente
async def verificar_pagamento(update, context):
    user_id = update.message.from_user.id
    
    if user_id in usuarios_pagos:
        await update.message.reply_text("✅ Pagamento confirmado! Você já pode acessar o grupo.")
    else:
        await update.message.reply_text("⏳ Seu pagamento ainda não foi confirmado. Aguarde ou entre em contato.")

# Configuração do bot
def main():
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Adiciona comandos ao bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("verificar", verificar_pagamento))

    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()
