import os
import sys
import logging
from tgbot.nuaa import startinuaa 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


TOKEN = os.getenv("TOKEN")
MODE = os.getenv("MODE")
DATA_FILE_NAME = 'data.json'
PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def start(update, context):
    update.message.reply_text('欢迎使用 🎉')

def help(update, context):
    update.message.reply_text('我是人见人爱的yym的小跟班~')

def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# def inuaa(update: Update, context: CallbackContext):
#     result = startinuaa(context.args[0], context.args[1])
#     context.bot.send_message(chat_id=update.effective_chat.id, text=result)

if __name__ == '__main__':
    if MODE == "dev":
        updater = Updater(TOKEN, use_context=True, request_kwargs={
            'proxy_url': 'https://127.0.0.1:7890' # 如果你需要翻墙才能使用 telegram 需要设置 vpn 软件中使用的代理设置
        })
    elif MODE == "prod":
        updater = Updater(TOKEN, use_context=True)
    else:
        logger.error("需要设置 MODE!")
        sys.exit(1)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("caps", caps))
    # dispatcher.add_handler(CommandHandler("inuaa", inuaa))

    # dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_error_handler(error)

    if MODE == "dev":
        updater.start_polling()
    elif MODE == "prod":
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    updater.idle()