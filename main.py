import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.getenv("TOKEN")
DATA_FILE_NAME = 'data.json'
MODE = os.getenv("MODE")
PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
WHITE_LIST = os.getenv("WHITE_LIST")
logger = logging.getLogger()

def start(update, context):
    update.message.reply_text('欢迎使用 🎉')

def help(update, context):
    update.message.reply_text('Help!')

def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True, request_kwargs={
        'proxy_url': 'HTTPS://127.0.0.1:7890/'
    })

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    dispatcher.add_error_handler(error)

    if MODE == "dev":
        updater.start_polling()
    elif MODE == "prod":
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    # updater.start_polling()
    updater.idle()