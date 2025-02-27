from telegram import Update
from telegram.ext import CallbackContext
from database import verificar_assinatura

def pagamento_confirmado(update: Update, context: CallbackContext, user_id: int):
    assinatura = verificar_assinatura(user_id)
    if not assinatura:
        return
    
    user_id, plano, metodo, data_inicio, status = assinatura
    
    # Links específicos para cada plano
    links = {
        "mensal": "https://t.me/addlist/K8OVwB0BM_pmMzcx",
        "anual": "https://t.me/addlist/K8OVwB0BM_pmMzcx\nhttps://t.me/+additional_annual_channel",
        "vitalicia": "https://t.me/addlist/K8OVwB0BM_pmMzcx\nhttps://t.me/+vip_lifetime_channel\nhttps://t.me/+exclusive_content",
        "sugestao_extra": "https://t.me/addlist/K8OVwB0BM_pmMzcx\nhttps://t.me/+extra_suggestion_channel"
    }
    
    mensagens = {
        "mensal": "🎉 Bem-vindo ao Plano Mensal!",
        "anual": "🌟 Bem-vindo ao Plano Anual! Aproveite benefícios exclusivos!",
        "vitalicia": "👑 Bem-vindo ao Plano Vitalício! Você agora tem acesso total!",
        "sugestao_extra": "💎 Bem-vindo ao Plano Sugestão Extra!"
    }
    
    context.bot.send_message(
        chat_id=user_id,
        text=f"""✨ Pagamento confirmado! {mensagens[plano]}

🎁 Aqui estão seus acessos exclusivos:
📱 Seus canais VIP:
{links[plano]}

⭐ Aproveite seu conteúdo exclusivo!""")
