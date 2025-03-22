from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Função que será chamada quando o comando /start for executado
async def start(update: Update, context: CallbackContext):
    # Limpa os dados do usuário para garantir um novo cálculo
    context.user_data.clear()

    # Criando os botões de seleção
    keyboard = [
        [InlineKeyboardButton("Arbitragem Bidimensional (2 odds)", callback_data='bidimensional')],
        [InlineKeyboardButton("Arbitragem Tri-dimensional (3 odds)", callback_data='tridimensional')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Mensagem inicial com botões
    await update.message.reply_text(
        "Olá! Eu sou o seu assistente de apostas!\n"
        "Vamos calcular o dutching para as suas apostas. Vamos começar? 😊\n\n"
        "Escolha o tipo de arbitragem que deseja:", 
        reply_markup=reply_markup
    )

# Função que processa a escolha do tipo de arbitragem (bidimensional ou tri-dimensional)
async def escolha_arbitragem(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Verifica qual opção foi escolhida
    escolha = query.data

    if escolha == 'bidimensional':
        await query.edit_message_text(
            "Você escolheu Arbitragem Bidimensional. Vamos começar!\n"
            "Por favor, me envie a odd desregulada (Odd 1):"
        )
        context.user_data['arbitragem'] = 'bidimensional'
        context.user_data['etapa'] = 'odd1'

    elif escolha == 'tridimensional':
        await query.edit_message_text(
            "Você escolheu Arbitragem Tri-dimensional. Vamos começar!\n"
            "Por favor, me envie a odd desregulada (Odd 1):"
        )
        context.user_data['arbitragem'] = 'tridimensional'
        context.user_data['etapa'] = 'odd1'

# Função para calcular a lucratividade
def calcular_lucratividade(odds, stakes):
    total_investido = sum(stakes)
    retorno_total = max([stakes[i] * odds[i] for i in range(len(odds))])  # Apenas a odd vencedora
    lucro = retorno_total - total_investido
    return lucro

# Função para processar as odds e calcular
async def processar_apostas(update: Update, context: CallbackContext):
    user_input = update.message.text
    arbitragem = context.user_data.get('arbitragem')
    etapa = context.user_data.get('etapa')

    try:
        if etapa == 'odd1':
            context.user_data['odd1'] = float(user_input)
            context.user_data['etapa'] = 'stake1'
            await update.message.reply_text(
                f"Você enviou a Odd 1: {user_input}. Agora, me envie o valor apostado na Odd 1 (ex: 100):"
            )
        
        elif etapa == 'stake1':
            context.user_data['stake1'] = float(user_input)
            if arbitragem == 'bidimensional':
                context.user_data['etapa'] = 'odd2'
                await update.message.reply_text(
                    f"Você apostou R${user_input} na Odd 1. Agora, me envie a odd de proteção (Odd 2):"
                )
            elif arbitragem == 'tridimensional':
                context.user_data['etapa'] = 'odd2'
                await update.message.reply_text(
                    f"Você apostou R${user_input} na Odd 1. Agora, me envie a segunda odd (Odd 2):"
                )
        
        elif etapa == 'odd2':
            context.user_data['odd2'] = float(user_input)
            if arbitragem == 'bidimensional':
                odd1 = context.user_data['odd1']
                odd2 = context.user_data['odd2']
                stake1 = context.user_data['stake1']
                
                # Calculando a stake2 para arbitragem bidimensional
                stake2 = (odd1 * stake1) / odd2
                stakes = [stake1, stake2]
                odds = [odd1, odd2]
                
                # Calculando a lucratividade
                lucro = calcular_lucratividade(odds, stakes)
                
                # Exibindo o resultado
                resultado_msg = (
                    f"🔢 **Resultados do cálculo de arbitragem Bidimensional** 🔢\n\n"
                    f"✅ **Odd 1**: {odd1}\n"
                    f"💰 **Valor apostado na Odd 1**: R${stake1:.2f}\n"
                    f"✅ **Odd 2 (Proteção)**: {odd2}\n"
                    f"💰 **Valor apostado na Odd 2**: R${stake2:.2f}\n\n"
                    f"📊 **Retorno**:\n"
                )
                if lucro > 0:
                    resultado_msg += f"🟢🟢🟢 **Lucro**: R${lucro:.2f} 🟢🟢🟢\n"
                else:
                    resultado_msg += f"🔴🔴🔴 APOSTA NÃO SERÁ LUCRATIVA 🔴🔴🔴\n🔴🔴🔴 **Prejuízo**: R${-lucro:.2f} 🔴🔴🔴\n"
                
                await update.message.reply_text(resultado_msg)
                await start(update, context)  # Reinicia o bot

            elif arbitragem == 'tridimensional':
                context.user_data['etapa'] = 'odd3'
                await update.message.reply_text(
                    f"Você enviou a Odd 2: {user_input}. Agora, me envie a **terceira odd** (Odd 3):"
                )
        
        elif etapa == 'odd3':
            context.user_data['odd3'] = float(user_input)
            odd1 = context.user_data['odd1']
            odd2 = context.user_data['odd2']
            odd3 = context.user_data['odd3']
            stake1 = context.user_data['stake1']
            
            # Calculando stake2 e stake3 para arbitragem tri-dimensional
            stake2 = (odd1 * stake1) / odd2
            stake3 = (odd1 * stake1) / odd3
            stakes = [stake1, stake2, stake3]
            odds = [odd1, odd2, odd3]
            
            # Calculando a lucratividade
            lucro = calcular_lucratividade(odds, stakes)
            
            # Exibindo o resultado
            resultado_msg = (
                f"🔢 **Resultados do cálculo de arbitragem Tri-dimensional** 🔢\n\n"
                f"✅ **Odd 1**: {odd1}\n"
                f"💰 **Valor apostado na Odd 1**: R${stake1:.2f}\n"
                f"✅ **Odd 2 (Proteção)**: {odd2}\n"
                f"💰 **Valor apostado na Odd 2**: R${stake2:.2f}\n"
                f"✅ **Odd 3**: {odd3}\n"
                f"💰 **Valor apostado na Odd 3**: R${stake3:.2f}\n\n"
                f"📊 **Retorno**:\n"
            )
            if lucro > 0:
                resultado_msg += f"🟢🟢🟢 **Lucro**: R${lucro:.2f} 🟢🟢🟢\n"
            else:
                resultado_msg += f"🔴🔴🔴 APOSTA NÃO SERÁ LUCRATIVA 🔴🔴🔴\n🔴🔴🔴 **Prejuízo**: R${-lucro:.2f} 🔴🔴🔴\n"
            
            await update.message.reply_text(resultado_msg)
            await start(update, context)  # Reinicia o bot

    except ValueError:
        await update.message.reply_text("Por favor, insira um número válido.")

# Função principal para configurar e rodar o bot
def main():
    # Substitua "SEU_TOKEN_AQUI" pelo token do seu bot fornecido pelo BotFather
    application = Application.builder().token("7534618063:AAFn2gQ6Thb2n76Jy0dbnTOyQeZDICDUkOI").build()

    # Registra o comando /start
    application.add_handler(CommandHandler("start", start))
    
    # Registra o handler para a seleção dos botões de arbitragem
    application.add_handler(CallbackQueryHandler(escolha_arbitragem))
    
    # Registra as funções de cálculo
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_apostas))

    # Inicia o bot
    application.run_polling()

if __name__ == "__main__":
    main()