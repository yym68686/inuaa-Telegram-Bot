import os
import sys
import json
import asyncio
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
TOKEN = os.getenv("TOKEN")
DATA_FILE_NAME = 'data.json'
MODE = os.getenv("MODE")
PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
WHITE_LIST = os.getenv("WHITE_LIST")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def readFile(file):
    try:
        with open(file, 'r') as handle:
            data = json.load(handle)
            handle.close()

            if data:
                return data
            else:
                return {}
    except FileNotFoundError:
        file = open(DATA_FILE_NAME, 'w')
        file.close()
        return {}

async def writeToFile(file, dict):
    with open(file, 'w') as handle: # w 表示每次写时覆盖原内容
        json.dump(dict, handle)
        handle.write("\n")
        handle.close()

def start(update, context):
    update.message.reply_text('欢迎使用 🎉')

def help(update, context):
    update.message.reply_text('Help!')

def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# 用户会对应一些业务，每个业务对应该用户的选择
def subscriptionCallback(update, context):
    query = update.callback_query
    query.edit_message_text(text="订阅成功 🎉")

    chatId = str(query.message.chat.id)

    data = readFile(DATA_FILE_NAME)

    if chatId in data.keys():
        userData = data[chatId]

        if 'subscription' in userData:
            userSubscription = userData['subscription']

            if query.data not in userSubscription:
                userSubscription.append(query.data)
                data[chatId]['subscription'] = userSubscription
        else:
            data[chatId].append({'subscription': [query.data]})
    else:
        data[chatId] = {'subscription': [query.data]}

    asyncio.run(writeToFile(DATA_FILE_NAME, data))

if __name__ == '__main__':
    if MODE == "dev":
        updater = Updater(TOKEN, use_context=True, request_kwargs={
            'proxy_url': 'socks5h://127.0.0.1:7890' # 如果你需要翻墙才能使用 telegram 需要设置 vpn 软件中使用的代理设置
        })
    elif MODE == "prod":
        updater = Updater(TOKEN, use_context=True)
    else:
        logger.error("需要设置 MODE!")
        sys.exit(1)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CallbackQueryHandler(subscriptionCallback))

    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    dispatcher.add_error_handler(error)

    if MODE == "dev":
        updater.start_polling()
    elif MODE == "prod":
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    # updater.start_polling()
    updater.idle()