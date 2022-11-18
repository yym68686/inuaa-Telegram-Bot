import os
import sys
import time
import logging
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, filters

# TOKEN = os.getenv("TOKEN") # 从环境变量自动获取telegram bot Token
TOKEN = "5569497961:AAHobhUuydAwD8SPkXZiVFybvZJOmGrST_w"
PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# In all other places characters
# _ * [ ] ( ) ~ ` > # + - = | { } . ! 
# must be escaped with the preceding character '\'.
def start(update, context): # 当用户输入/start时，返回文本
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()} 欢迎使用 🎉",
        # reply_markup=ForceReply(selective=True),
    )
    message = (
        "我是人见人爱的yym的小跟班\~\n\n"
    )
    update.message.reply_text(message, parse_mode='MarkdownV2')

# 小功能
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    if ("timeout" in str(context.error) or "TIMED_OUT" in str(context.error)):
        message = (
            f"用户名或密码错误！请重试\n\n"
            f"若无法申请成功，请联系 @yym68686\n\n"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='MarkdownV2')


def echo(update, context):
    # updater.bot.send_message(chat_id = update.effective_chat.id, text= str(update.effective_chat.id) + " " + update.message.text)
    update.message.reply_text(update.message.text)

def unknown(update: Update, context: CallbackContext): # 当用户输入未知命令时，返回文本
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    # updater = Updater(TOKEN, use_context=True)
    updater = Updater(TOKEN, use_context=True, request_kwargs={
        'proxy_url': 'http://127.0.0.1:6152' # 需要代理才能使用 telegram
    })

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    # 其他小功能
    dispatcher.add_handler(CommandHandler("echo", echo))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_error_handler(error)

    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://bot.yym68686.top/{}".format(TOKEN))
    updater.idle()