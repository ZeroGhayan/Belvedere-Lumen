# handlers/vip.py
import json
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from payments.mercado_pago import gerar_pagamento_mp, verificar_pagamento_mp
from payments.paypal import gerar_pagamento_paypal
from payments.zbd import gerar_pagamento_zbd
from database import adicionar_assinatura

# Caminho para o arquivo JSON
CAMINHO_CANAIS = os.path.join(os.path.dirname(__file__), "..", "canais.json")

def carregar_canais():
    """Carrega a lista de canais a partir do arquivo JSON."""
    try:
        with open(CAMINHO_CANAIS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception as e:
        print(f"Erro ao carregar canais: {e}")
        return {}

# Carrega os canais
CANAIS = carregar_canais()

PLANOS = {
    "mensal": {"nome": "Mensal", "multiplicador": 1, "base": 10},
    "anual": {"nome": "Anual", "multiplicador": 10, "base": 100},
    "vitalicio": {"nome": "Vitalício", "multiplicador": 50, "base": 500}
}

def vip_command(update, context):
    keyboard = []
    for canal_id, info in CANAIS.items():
        keyboard.append([InlineKeyboardButton(
            f"{info['nome']}", 
            callback_data=f'canal_{canal_id}'
        )])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        '📺 Escolha o canal que deseja acessar:\n\n'
        '💡 Você também pode ter acesso a todos os canais ou sugerir um novo!', 
        reply_markup=reply_markup
    )

def mostrar_planos(update, context):
    query = update.callback_query
    query.answer()

    _, canal_escolhido = query.data.split('_', 1)
    context.user_data['canal'] = canal_escolhido

    # Definir multiplicador baseado na escolha do canal
    multiplicador = (len(CANAIS)-2) if canal_escolhido == 'todos_canais' else 1
    multiplicador = ((len(CANAIS)-2)//2) if canal_escolhido == 'sugestao' else multiplicador

    keyboard = []
    for plano_id, info in PLANOS.items():
        valor = info['base'] * multiplicador
        keyboard.append([InlineKeyboardButton(
            f"{info['nome']} - R${valor:.2f}", 
            callback_data=f'plano_{plano_id}'
        )])

    reply_markup = InlineKeyboardMarkup(keyboard)
    canal_nome = CANAIS[canal_escolhido]['nome']
    query.edit_message_text(
        f"Canal escolhido: {canal_nome}\n"
        f"Escolha seu plano:", 
        reply_markup=reply_markup
    )

def escolher_metodo_pagamento(update, context):
    query = update.callback_query
    query.answer()

    plano = query.data.replace('plano_', '')
    canal = context.user_data.get('canal')
    context.user_data['plano'] = plano

    # Calcular valor final
    multiplicador = (len(CANAIS)-2)//1+(((len(CANAIS)-2)//10)) if canal == 'todos_canais' else 1
    multiplicador = ((len(CANAIS)-2)//2)//1+(((len(CANAIS)-2)//10)) if canal == 'sugestao' else multiplicador
    valor = PLANOS[plano]['base'] * multiplicador
    context.user_data['valor'] = valor

    keyboard = [
        [InlineKeyboardButton("Mercado Pago", callback_data='mercado_pago')],
        [InlineKeyboardButton("PayPal", callback_data='paypal')],
        [InlineKeyboardButton("Bitcoin (Lightning)", callback_data='zbd')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        f"Canal: {CANAIS[canal]['nome']}\n"
        f"Plano: {PLANOS[plano]['nome']}\n"
        f"Valor: R${valor:.2f}\n\n"
        f"Escolha o método de pagamento:", 
        reply_markup=reply_markup
    )

def processar_pagamento(update, context):
    try:
        query = update.callback_query
        query.answer()
        metodo_pagamento = query.data

        if 'canal' not in context.user_data or 'plano' not in context.user_data:
            query.edit_message_text("Erro: Seleção incompleta. Por favor, comece novamente com /vip")
            return

        canal = context.user_data['canal']
        plano = context.user_data['plano']
        valor = context.user_data['valor']
        user_id = query.from_user.id
        link_pagamento = None

        try:
            if metodo_pagamento == 'mercado_pago':
                link_pagamento = gerar_pagamento_mp(valor, f"Assinatura {plano} - {CANAIS[canal]['nome']}", user_id, CANAIS[canal]['link'])
            elif metodo_pagamento == 'paypal':
                link_pagamento = gerar_pagamento_paypal(valor, f"Assinatura {plano} - {CANAIS[canal]['nome']}")
            elif metodo_pagamento == 'zbd':
                link_pagamento = gerar_pagamento_zbd(valor * 1000, f"Assinatura {plano} - {CANAIS[canal]['nome']}")
        except Exception as e:
            print(f"Erro ao gerar pagamento {metodo_pagamento}: {str(e)}")
            query.edit_message_text(f"Erro ao gerar pagamento via {metodo_pagamento}. Por favor, tente outro método de pagamento ou contacte o suporte.")
            return

        if link_pagamento:
            try:
                # Adiciona a assinatura ao banco de dados
                canal_id = CANAIS[canal]['link']
                adicionar_assinatura(user_id, plano, metodo_pagamento, canal_id)

                # Envia o link do canal após o pagamento
                link_grupo = CANAIS[canal]['link']
                query.edit_message_text(
                    f"✨ Link de pagamento gerado!\n\n"
                    f"💰 Valor: R${valor:.2f}\n"
                    f"📺 Canal: {CANAIS[canal]['nome']}\n"
                    f"📦 Plano: {PLANOS[plano]['nome']}\n\n"
                    f"🔗 Link para pagamento:\n{link_pagamento}\n\n"
                    f"⚠️ Após o pagamento, você receberá uma confirmação."
                )

                # Verifica o status do pagamento (simulação)
                if metodo_pagamento == 'mercado_pago':
                    pagamento_aprovado = verificar_pagamento_mp(user_id, canal_id)
                    if pagamento_aprovado:
                        context.bot.send_message(chat_id=user_id, text=f"✅ Pagamento aprovado! Acesse o canal aqui: {link_grupo}")
                    else:
                        context.bot.send_message(chat_id=user_id, text="❌ Pagamento não aprovado. Tente novamente.")
            except sqlite3.IntegrityError:
                query.edit_message_text("Você já possui uma assinatura ativa. Use /cancel para cancelar a atual antes de criar uma nova.")
            except Exception as e:
                print(f"Erro ao adicionar assinatura: {str(e)}")
                query.edit_message_text("Erro ao registrar assinatura. Por favor, contacte o suporte.")
        else:
            query.edit_message_text("Não foi possível gerar o link de pagamento. Por favor, tente outro método de pagamento.")

    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        if update and update.callback_query:
            update.callback_query.edit_message_text("Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.")

def setup_vip_handlers(dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(mostrar_planos, pattern='^canal_'))
    dispatcher.add_handler(CallbackQueryHandler(escolher_metodo_pagamento, pattern='^plano_'))
    dispatcher.add_handler(CallbackQueryHandler(processar_pagamento, pattern='^(mercado_pago|paypal|zbd)$'))