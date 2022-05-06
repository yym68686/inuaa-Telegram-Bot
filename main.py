import os
import sys
import logging
from nuaa import startinuaa
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.getenv("TOKEN") # 从环境变量自动获取telegram bot Token
MODE = os.getenv("MODE")
PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def start(update, context): # 当用户输入/start时，返回文本
    update.message.reply_text('欢迎使用 🎉')

def help(update, context):
    update.message.reply_text('我是人见人爱的yym的小跟班~')

def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def unknown(update: Update, context: CallbackContext): # 当用户输入未知命令时，返回文本
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def caps(update: Update, context: CallbackContext): # 小的测试功能，也是官方示例，将用户参数转化为大写
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def inuaa(update: Update, context: CallbackContext): # 当用户输入/inuaa 学号，密码 时，自动打卡，调用nuaa.py文件
    if (len(context.args) == 2): # /inuaa后面必须是两个参数
        context.bot.send_message(chat_id=update.effective_chat.id, text="请稍等哦，大约20秒就好啦~")
        result = startinuaa(context.args[0], context.args[1]) # 调用打卡程序
        context.bot.send_message(chat_id=update.effective_chat.id, text=result) # 打卡结果打印
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="格式错误哦~，请输入 /inuaa <学号> <教务处密码>，例如学号为123，密码是123，则输入/inuaa 123 123")


if __name__ == '__main__':
    if MODE == "dev": # 本地调试，需要挂代理，这里使用的是Clash
        updater = Updater(TOKEN, use_context=True, request_kwargs={
            'proxy_url': 'https://127.0.0.1:7890' # 需要代理才能使用 telegram
        })
    elif MODE == "prod": # 生产服务器在美国，不需要代理
        updater = Updater(TOKEN, use_context=True)
    else:
        logger.error("需要设置 MODE!")
        sys.exit(1)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("caps", caps))
    dispatcher.add_handler(CommandHandler("inuaa", inuaa)) # 当用户输入/inuaa时，调用inuaa()函数

    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_error_handler(error)

    if MODE == "dev": # 本地调试
        updater.start_polling()
    elif MODE == "prod": # HeroKu 远程生产环境
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    updater.idle()