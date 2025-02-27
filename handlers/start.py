# handlers/start.py
from database import adicionar_usuario  # Removemos a importação desnecessária
from datetime import datetime

def start_command(update, context):
    message = """
    ✨ Olá! Bem-vindo docinho! 🌟

    🔥 Atualmente, temos as seguintes estrelas disponíveis:
    👑 Summer Hart
    💫 Amira West
    💎 Babylyraxxx
    🌙 Tokyo.teaa
    ⭐ KabsCorner
    🔺 SweetieFox_OF

    💝 Comandos disponíveis:
    🎯 /vip - Assine e acesse ofertas e canais exclusivos
    🔺 /flix - verifica sua assinatura atual
    ❌ /cancel - Cancele sua assinatura
    🎁 /all - Acesse o canal gratuito com prévias
    """
    update.message.reply_text(message)

    # Adiciona o usuário ao banco de dados (ocultamente)
    user = update.message.from_user
    adicionar_usuario(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )