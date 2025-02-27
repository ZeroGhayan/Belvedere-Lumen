# handlers/cancel.py
from telegram import Update
from telegram.ext import CallbackContext
from database import cancelar_assinatura, verificar_assinaturas_usuario

def cancel_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Verifica se o usuário tem uma assinatura ativa
    assinaturas = verificar_assinaturas_usuario(user_id)
    if assinaturas:
        for assinatura in assinaturas:
            canal_id = assinatura['canal_id']
            cancelar_assinatura(user_id, canal_id)
        mensagem = "Todas as suas assinaturas foram canceladas com sucesso."
    else:
        mensagem = "Você não possui assinaturas ativas."

    # Envia a mensagem de confirmação para o usuário
    update.message.reply_text(mensagem)