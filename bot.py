from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context): # 当用户输入/start时，返回文本
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()} 欢迎使用 🎉",
    )

def echo(update, context):
    update.message.reply_text(update.message.text)

def setup(token):
    updater = Updater(token, use_context=True, request_kwargs={
        'proxy_url': 'http://127.0.0.1:6152' # 需要代理才能使用 telegram
    })

    dispatcher = updater.dispatcher

    # 其他小功能
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    return updater, dispatcher
