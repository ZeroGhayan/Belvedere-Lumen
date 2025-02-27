from telegram.ext import CommandHandler
from database import atualizar_status_assinatura

def handle_payment_status(update, context):
    args = context.args
    if not args:
        return
        
    status = args[0]
    user_id = update.effective_user.id
    
    if status == "payment_success":
        context.bot.send_message(
            chat_id=user_id,
            text="✅ Pagamento confirmado! Seu acesso será liberado em instantes."
        )
        atualizar_status_assinatura(user_id, "ativo")
        
    elif status == "payment_pending":
        context.bot.send_message(
            chat_id=user_id,
            text="⏳ Pagamento pendente!\n\n"
                 "Assim que confirmarmos o pagamento, seu acesso será liberado automaticamente.\n"
                 "Use /flix para verificar o status do seu pagamento."
        )
        atualizar_status_assinatura(user_id, "pendente")
        
    elif status == "payment_failed":
        context.bot.send_message(
            chat_id=user_id,
            text="❌ Pagamento não aprovado!\n\n"
                 "Você pode tentar novamente usando o comando /vip\n"
                 "Se precisar de ajuda, entre em contato com nosso suporte."
        )
        atualizar_status_assinatura(user_id, "falhou")
