import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.getenv("TOKEN")
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

    updater.start_polling()
    updater.idle()