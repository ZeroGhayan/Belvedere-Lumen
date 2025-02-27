# handlers/all.py
from telegram import Update
from telegram.ext import CallbackContext

def all_command(update: Update, context: CallbackContext):
    # Link do canal gratuito
    canal_link = "https://t.me/+z3BneibjH_1lMDYx"
    
    # Mensagem para o usuário
    mensagem = f"Clique no link abaixo para entrar no canal gratuito:\n\n{canal_link}"
    
    # Envia a mensagem com o link do canal
    update.message.reply_text(mensagem)