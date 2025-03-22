from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Função que inicia o bot
async def start(update: Update, context: CallbackContext):
    context.user_data.clear()  # Limpa dados anteriores
    
    keyboard = [[InlineKeyboardButton("Calcular Aposta de Valor", callback_data='calcular_ev')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎲 Olá! Eu sou o seu assistente de apostas de valor! 🎲\n\n"
        "Clique abaixo para iniciar:",
        reply_markup=reply_markup
    )

# Função que processa a escolha do usuário
async def escolha_calculo(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("📌 Digite a odd de referência (de uma casa confiável):")
    context.user_data['etapa'] = 'odd_referencia'

# Função que processa os valores enviados pelo usuário
async def processar_apostas(update: Update, context: CallbackContext):
    user_input = update.message.text
    etapa = context.user_data.get('etapa')

    try:
        if etapa == 'odd_referencia':
            odd_ref = float(user_input)
            if odd_ref <= 1:
                await update.message.reply_text("❌ A odd de referência deve ser maior que 1. Tente novamente.")
                return
            context.user_data['odd_referencia'] = odd_ref
            context.user_data['etapa'] = 'odd_aposta'
            await update.message.reply_text("📌 Agora, digite a odd da casa onde você quer apostar:")

        elif etapa == 'odd_aposta':
            odd_aposta = float(user_input)
            if odd_aposta <= 1:
                await update.message.reply_text("❌ A odd da aposta deve ser maior que 1. Tente novamente.")
                return
            context.user_data['odd_aposta'] = odd_aposta

            # Pega os valores armazenados
            odd_ref = context.user_data['odd_referencia']
            odd_aposta = context.user_data['odd_aposta']

            # Calcula probabilidade e EV
            prob_real = 1 / odd_ref
            ev = (prob_real * odd_aposta) - 1

            # Calcula stake baseada em uma versão conservadora do Critério de Kelly
            if ev > 0:
                fator_conservadorismo = 0.17  # Fator para garantir 6% no exemplo dado
                stake_percentual = (ev / (odd_aposta - 1)) * fator_conservadorismo
                stake = stake_percentual * 100  # Converte para porcentagem da banca
            else:
                stake = 0

            # Limita a stake máxima a 10% da banca (ajuste conforme necessário)
            if stake > 10:
                stake = 10

            # Formata a resposta
            resposta = (
                f"📊 **Resultados da Aposta de Valor** 📊\n\n"
                f"✅ **Odd de Referência**: {odd_ref}\n"
                f"✅ **Odd da Aposta**: {odd_aposta}\n"
                f"📌 **Probabilidade Estimada**: {prob_real:.2%}\n"
                f"📌 **EV Calculado**: {ev:.3f}\n"
                f"💰 **Unidade Sugerida (SEMPRE APROXIME A UNIDADE)**: {stake:.2f}u da banca"
            )

            if ev > 0:
                resposta += "\n🟢 **APOSTA TEM VALOR!**"
            else:
                resposta += "\n🔴 **APOSTA NÃO TEM VALOR!**"

            await update.message.reply_text(resposta)
            await start(update, context)  # Reinicia o bot

    except ValueError:
        await update.message.reply_text("❌ Entrada inválida! Digite um número válido.")

# Função principal para rodar o bot
def main():
    application = Application.builder().token("7557426257:AAGpjPHG08OU1B_lVO7kSrQ7TiUYjyBVexQ").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(escolha_calculo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_apostas))

    application.run_polling()

if __name__ == "__main__":
    main()