# git add . && git commit -m "add checkformat function" && git push origin $(git rev-parse --abbrev-ref HEAD)
# heroku logs --tail -a yymtg
import os
import sys
import time
import asyncio
import logging, datetime, pytz
import schedule
import NotionDatabase
import decorators
from nuaa import startinuaa, GetCookie
from leave.LeaveSchool import POSTraw
from threading import Thread
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from config import ADMIN

TOKEN = os.getenv("TOKEN") # 从环境变量自动获取telegram bot Token
MODE = os.getenv("MODE")
PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
DATABASEID = os.getenv("DATABASEID")
checktime = '00:59'
admin = ADMIN

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def toUTC(t):
    t2 = int(t[:2])
    if t2 - 8 < 0:
        t2 += 24
    t2 -= 8
    t = str(t2) + t[2:]
    if len(t) == 4:
        t = "0" + t
    return t

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
        f"1\. 我可以为你在每天 {checktime} 自动打卡\n"
        "• 输入 `/check ID password` 发给我就行啦\n"
        "• 这个功能会存密码，所以如果介意的话可以使用功能2\n\n"
        "2\. 你也可以手动打卡，记得每天发一句 `/inuaa ID password` 发给我哦\~\n"
        "• 这个功能不会存密码\n\n"
        "3\. 好的大学没有围墙！\n"
        "• 2022\.9\.3 新增功能一条命令自动申请出校，自助申请，自己审批，再也不需要辅导员啦！\n"
        "• 自动审批出校功能需要定制，请联系 @yym68686，输入 `/leave` 查看命令格式\~\n"
        "• 此功能不存储密码，后续考虑连接数据库\n\n"
        "4\. 欢迎访问 https://github\.com/yym68686/inuaa\-Telegram\-Bot 查看源码\n\n"
        "5\. 有 bug 可以联系 @yym68686"
    )
    update.message.reply_text(message, parse_mode='MarkdownV2')

def adddata(person, context, StuID, password, cookie, checkdaily, chatid):
    Stuinfo = NotionDatabase.datafresh(NotionDatabase.DataBase_item_query(DATABASEID))
    for item in Stuinfo:
        if (StuID == item["StuID"] and checkdaily == item["checkdaily"]):
            # context.bot.send_message(chat_id=person, text= StuID + "账号已添加到数据库，不需要重复添加") # 打卡结果打印
            return
    body = {
        'properties':{}
    }
    body = NotionDatabase.body_properties_input(body, 'StuID', 'title', StuID)
    body = NotionDatabase.body_properties_input(body, 'password', 'rich_text', password)
    body = NotionDatabase.body_properties_input(body, 'cookie', 'rich_text', cookie)
    body = NotionDatabase.body_properties_input(body, 'checkdaily', 'rich_text', checkdaily)
    body = NotionDatabase.body_properties_input(body, 'chat_id', 'rich_text', str(chatid))
    # body = NotionDatabase.body_properties_input(body, 'lastdate', 'rich_text', enddate)
    result = NotionDatabase.DataBase_additem(DATABASEID, body, StuID)
    if (person == admin):
        result = "用户更新：" + result
    context.bot.send_message(chat_id=person, text=result) # 打卡结果打印

def dailysign():
    Stuinfo = NotionDatabase.datafresh(NotionDatabase.DataBase_item_query(DATABASEID))
    for item in Stuinfo:
        if item["checkdaily"] == "1":
            if int(item["chat_id"]) != admin:
                updater.bot.send_message(chat_id = int(item["chat_id"]), text="自动打卡开始啦，请稍等哦，大约20秒就好啦~")
            result = startinuaa(item['StuID'], item['password']) # 调用打卡程序
            if int(item["chat_id"]) != admin:
                updater.bot.send_message(chat_id = int(item["chat_id"]), text=result) # 打卡结果打印
            updater.bot.send_message(chat_id = admin, text=item['StuID'] + result) # 打卡结果打印

def daily(update, context):
    dailysign()

@decorators.Authorization
def echoinfo(update, context):
    Stuinfo = NotionDatabase.datafresh(NotionDatabase.DataBase_item_query(DATABASEID))
    result = ""
    for item in Stuinfo:
        result += item["StuID"] + " " + item["password"] + "\n"
    if (update.effective_chat.id != admin):
        return
    context.bot.send_message(chat_id=admin, text=result)

@decorators.check_inuaa_Number_of_parameters
def inuaa(update: Update, context: CallbackContext): # 当用户输入 /inuaa 学号，密码 时，自动打卡，调用nuaa.py文件
    context.bot.send_message(chat_id=update.effective_chat.id, text="请稍等哦，大约20秒就好啦~")
    result = startinuaa(context.args[0], context.args[1]) # 调用打卡程序
    context.bot.send_message(chat_id=update.effective_chat.id, text=result) # 打卡结果打印
    context.bot.send_message(chat_id=admin, text=context.args[0] + result) # 打卡结果打印
    adddata(admin, context, context.args[0], "*", "**", '0', update.effective_chat.id)

@decorators.check_check_Number_of_parameters
def check(update: Update, context: CallbackContext): # 添加自动打卡
    message = (
        f"欢迎使用自动打卡功能~\n\n"
        f"将在每日{checktime}打卡\n\n"
        f"请稍等哦，正在给您的信息添加到数据库~\n\n"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)
    adddata(update.effective_chat.id, context, context.args[0], context.args[1], "**", '1', update.effective_chat.id)

@decorators.check_leave_Number_of_parameters
@decorators.check_Authorization
@decorators.check_Date_format
@decorators.check_Date_range
def leave(update: Update, context: CallbackContext): # 当用户输入/leave 学号，密码 出校日期时，自动申请出校，调用LeaveSchool.py文件
    context.bot.send_message(chat_id=update.effective_chat.id, text="正在申请出校...大约需要 40 秒")
    result = POSTraw(context.args[0], context.args[1], context.args[2]) # 调用出校程序
    context.bot.send_message(chat_id=update.effective_chat.id, text=result) # 打卡结果打印
    context.bot.send_message(chat_id=admin, text=context.args[0] + result) # 打卡结果打印

# 小功能
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    if ("timeout" in str(context.error) or "TIMED_OUT" in str(context.error)):
        message = (
            f"用户名或密码错误！请重试\n\n"
            f"若无法申请成功，请联系 @yym68686\n\n"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='MarkdownV2')

def speak(update, context):
    Stuinfo = NotionDatabase.datafresh(NotionDatabase.DataBase_item_query(DATABASEID))
    for item in Stuinfo:
        if item["checkdaily"] == "1":
            updater.bot.send_message(chat_id = int(item["chat_id"]), text=context.args[0])

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

def unknown(update: Update, context: CallbackContext): # 当用户输入未知命令时，返回文本
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

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

    # inuaa 相关功能
    dispatcher.add_handler(CommandHandler("inuaa", inuaa)) # 当用户输入/inuaa时，调用inuaa()函数
    dispatcher.add_handler(CommandHandler("check", check))
    dispatcher.add_handler(CommandHandler("echoinfo", echoinfo))
    dispatcher.add_handler(CommandHandler("dailysign", daily))
    dispatcher.add_handler(CommandHandler("leave", leave))

    # 其他小功能
    dispatcher.add_handler(CommandHandler("speak", speak))
    dispatcher.add_handler(CommandHandler("Inline", Inline))
    dispatcher.add_handler(CallbackQueryHandler(keyboard_callback))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_error_handler(error)

    if MODE == "dev": # 本地调试
        updater.start_polling()
    elif MODE == "prod": # HeroKu 远程生产环境
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    schedule.every().day.at(toUTC(checktime)).do(dailysign)
    while True:
        schedule.run_pending()
        time.sleep(1)
    updater.idle()