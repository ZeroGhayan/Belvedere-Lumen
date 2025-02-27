# handlers/flix.py
def flix_command(update, context):
    # Verifica assinaturas ativas
    assinaturas = verificar_assinaturas_usuario(user_id)
    if assinaturas:
        mensagem = "📋 Suas assinaturas ativas:\n\n"
        for assinatura in assinaturas:
            canal_id = assinatura['canal_id']
            plano = assinatura['plano']
            data_fim = datetime.fromisoformat(assinatura['data_fim'])
            dias_restantes = (data_fim - datetime.now()).days
            mensagem += f"📺 Canal: {canal_id}\n"
            mensagem += f"📦 Plano: {plano}\n"
            mensagem += f"📅 Data início: {data_inicio.strftime('%d/%m/%Y %H:%M')}\n"
            mensagem += f"⏳ Dias restantes: {dias_restantes}\n\n"
    else:
        mensagem = "❌ Você não possui uma assinatura ativa!.\n Use /vip para assinar."

    update.message.reply_text(mensagem)