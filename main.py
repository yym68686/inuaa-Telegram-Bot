import os
import sys
import html
import time
import logging
import schedule
import NotionDatabase
from nuaa import startinuaa
from threading import Thread
from telegram import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

TOKEN = os.getenv("TOKEN") # 从环境变量自动获取telegram bot Token
MODE = os.getenv("MODE")

PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
DATABASEID = os.getenv("DATABASEID")
checktime = '18:05'

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def start(update, context): # 当用户输入/start时，返回文本
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()} 欢迎使用 🎉",
        reply_markup=ForceReply(selective=True),
    )

def help(update, context):
    message = (
        f"我是人见人爱的yym的小跟班~\n\n"
        f"1. 我可以为你在每天 {checktime} 自动打卡\n"
        f"输入 /check ID password 发给我就行啦\n"
        f"这个功能会存密码，所以如果介意的话可以使用功能2\n\n"
        f"2. 你也可以手动打卡，记得每天发一句 /inuaa ID password 发给我哦~\n"
        f"这个功能不会存密码\n\n"
        f"3. 欢迎访问https://github.com/yym68686/tgbot 查看源码\n\n"
        "4. 有 bug 可以联系 @yym68686"
    )
    update.message.reply_text(message)

def echo(update, context):
    update.message.reply_text(update.message.text)

def Inline(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [
            InlineKeyboardButton("Option 3", callback_data='3'),
        ]
    ] #1
    reply_markup = InlineKeyboardMarkup(keyboard) #2
    update.message.reply_text("Please choose:", reply_markup=reply_markup) #3


def keyboard_callback(update: Update, context: CallbackContext): #4
    query = update.callback_query #5
    query.answer() #6
    query.edit_message_text(text=f"Selected option: {query.data}") #7

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def unknown(update: Update, context: CallbackContext): # 当用户输入未知命令时，返回文本
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def caps(update: Update, context: CallbackContext): # 小的测试功能，也是官方示例，将用户参数转化为大写
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def check(update: Update, context: CallbackContext): # 添加自动打卡
    if (len(context.args) == 2): # /check 后面必须是两个参数
        message = (
            f"欢迎使用自动打卡功能~\n\n"
            f"将在每日{checktime}打卡\n\n"
            f"请稍等哦，正在给您的信息添加到数据库~\n\n"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)
        body = {
            'properties':{}
        }
        body = NotionDatabase.body_properties_input(body, 'StuID', 'title', context.args[0])
        body = NotionDatabase.body_properties_input(body, 'password', 'rich_text', context.args[1])
        body = NotionDatabase.body_properties_input(body, 'cookie', 'rich_text', '**')
        body = NotionDatabase.body_properties_input(body, 'checkdaily', 'rich_text', '1')
        body = NotionDatabase.body_properties_input(body, 'chat_id', 'rich_text', str(update.effective_chat.id))
        result = NotionDatabase.DataBase_additem(DATABASEID, body, context.args[0])
        context.bot.send_message(chat_id=update.effective_chat.id, text=result) # 打卡结果打印
    else:
        message = (
            f"格式错误哦~\n\n"
            f"请输入 <pre>/check 学号 教务处密码</pre>\n\n"
            f"例如学号为 123，密码是123\n\n"
            f"则输入 <pre>/check 123 123</pre>\n\n"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)

def dailysign():
    Stuinfo = NotionDatabase.datafresh(NotionDatabase.DataBase_item_query(DATABASEID))
    seen = set()
    Stuinfo = [x for x in Stuinfo if frozenset(x) not in seen and not seen.add(frozenset(x))]
    for item in Stuinfo:
        updater.bot.send_message(chat_id = int(item["chat_id"]), text="自动打卡开始啦，请稍等哦，大约20秒就好啦~")
        result = startinuaa(item['StuID'], item['password']) # 调用打卡程序
        updater.bot.send_message(chat_id = int(item["chat_id"]), text=result) # 打卡结果打印

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)

def inuaa(update: Update, context: CallbackContext): # 当用户输入/inuaa 学号，密码 时，自动打卡，调用nuaa.py文件
    if (len(context.args) == 2): # /inuaa后面必须是两个参数
        context.bot.send_message(chat_id=update.effective_chat.id, text="请稍等哦，大约20秒就好啦~")
        result = startinuaa(context.args[0], context.args[1]) # 调用打卡程序
        context.bot.send_message(chat_id=update.effective_chat.id, text=result) # 打卡结果打印
    else:
        message = (
            f"格式错误哦~\n\n"
            f"请输入 <pre>/inuaa 学号 教务处密码</pre>\n\n"
            f"例如学号为 123，密码是 123\n\n"
            f"则输入 <pre>/inuaa 123 123</pre>\n\n"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)

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
    dispatcher.add_handler(CommandHandler("Inline", Inline))
    dispatcher.add_handler(CommandHandler("check", check))
    dispatcher.add_handler(CallbackQueryHandler(keyboard_callback))
    dispatcher.add_handler(CommandHandler("inuaa", inuaa)) # 当用户输入/inuaa时，调用inuaa()函数

    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_error_handler(error)

    if MODE == "dev": # 本地调试
        updater.start_polling()
    elif MODE == "prod": # HeroKu 远程生产环境
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    schedule.every().day.at(checktime).do(dailysign)
    Thread(target=schedule_checker).start() 

    updater.idle()