# main.py
from telegram.ext import Updater, CommandHandler
from config import TOKEN
from handlers.start import start_command
from handlers.vip import vip_command, setup_vip_handlers
from handlers.all import all_command
from handlers.cancel import cancel_command
from handlers.flix import flix_command
from database import criar_banco_dados

def main():
    # Cria o banco de dados (se não existir)
    criar_banco_dados()

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Adiciona os comandos do bot
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("vip", vip_command))
    dp.add_handler(CommandHandler("all", all_command))
    dp.add_handler(CommandHandler("cancel", cancel_command))
    dp.add_handler(CommandHandler("flix", flix_command))

    # Configura os handlers de pagamento
    setup_vip_handlers(dp)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()