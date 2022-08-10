from http import cookies
import re
import os
import time
import logging
import requests
import NotionDatabase
from nuaa import startinuaa

from telegram import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

buttons = [
    [
        InlineKeyboardButton("DEL", callback_data="DEL"),
        InlineKeyboardButton("AC", callback_data="AC"),
    ],
    [
        InlineKeyboardButton("(", callback_data="("),
        InlineKeyboardButton(")", callback_data=")"),
    ],
    [
        InlineKeyboardButton("7", callback_data="7"),
        InlineKeyboardButton("8", callback_data="8"),
        InlineKeyboardButton("9", callback_data="9"),
        InlineKeyboardButton("/", callback_data="/"),
    ],
    [
        InlineKeyboardButton("4", callback_data="4"),
        InlineKeyboardButton("5", callback_data="5"),
        InlineKeyboardButton("6", callback_data="6"),
        InlineKeyboardButton("*", callback_data="*"),
    ],
    [
        InlineKeyboardButton("1", callback_data="1"),
        InlineKeyboardButton("2", callback_data="2"),
        InlineKeyboardButton("3", callback_data="3"),
        InlineKeyboardButton("-", callback_data="-"),
    ],
    [
        InlineKeyboardButton(".", callback_data="."),
        InlineKeyboardButton("0", callback_data="0"),
        InlineKeyboardButton("=", callback_data="="),
        InlineKeyboardButton("+", callback_data="+"),
    ],
]
banner = "@yym68686"
# banner = "{:.^34}".format(" Calculator by @odbots ")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        # reply_markup=InlineKeyboardMarkup(buttons), quote=True
        text=banner, reply_markup=InlineKeyboardMarkup(buttons), quote=True
    )


def calcExpression(text):
    try:
        return float(eval(text))
    except (SyntaxError, ZeroDivisionError):
        return ""
    except TypeError:
        return float(eval(text.replace('(', '*(')))
    except Exception as e:
        logger.error(e, exc_info=True)
        return ""


def button_press(update, context):
    """Function to handle the button press"""
    callback_query = update.callback_query
    callback_query.answer()
    text = callback_query.message.text.split("\n")[0].strip().split("=")[0].strip()
    text = '' if banner in text else text
    data = callback_query.data
    inpt = text + data
    result = ''
    if data == "=" and text:
        result = calcExpression(text)
        text = ""
    elif data == "DEL" and text:
        text = text[:-1]
    elif data == "AC":
        text = ""
    else:
        dot_dot_check = re.findall(r"(\d*\.\.|\d*\.\d+\.)", inpt)
        opcheck = re.findall(r"([*/\+-]{2,})", inpt)
        if not dot_dot_check and not opcheck:
            strOperands = re.findall(r"(\.\d+|\d+\.\d+|\d+)", inpt)
            if strOperands:
                text += data
                result = calcExpression(text)

    text = f"{text:<50}"
    if result:
        if text:
            text += f"\n{result:>50}"
        else:
            text = result
    text += '\n\n' + banner
    try:
        callback_query.edit_message_text(
            text=text, reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logger.info(e)
        pass

def help(update, context):
    message = (
        "我是人见人爱的yym的小跟班\~\n\n"
        f"1\. 我可以为你在每天 {checktime} 自动打卡\n"
        "输入 `/check ID password` 发给我就行啦\n"
        "这个功能会存密码，所以如果介意的话可以使用功能2\n\n"
        "2\. 你也可以手动打卡，记得每天发一句 `/inuaa ID password` 发给我哦\~\n"
        "这个功能不会存密码\n\n"
        "3\. 欢迎访问https://github\.com/yym68686/tgbot 查看源码\n\n"
        "4\. 有 bug 可以联系 @yym68686"
    )
    update.message.reply_text(message, parse_mode='MarkdownV2')


admin = 917527833
DATABASEID = os.getenv("DATABASEID")
def daily(update, context):
    Stuinfo = NotionDatabase.datafresh(NotionDatabase.DataBase_item_query(DATABASEID))
    for item in Stuinfo:
        if item["checkdaily"] == "1":
            if int(item["chat_id"]) != admin:
                context.bot.send_message(chat_id = int(item["chat_id"]), text="自动打卡开始啦，请稍等哦，大约20秒就好啦~")
            result = startinuaa(item['StuID'], item['password']) # 调用打卡程序
            if int(item["chat_id"]) != admin:
                context.bot.send_message(chat_id = int(item["chat_id"]), text=result) # 打卡结果打印
            context.bot.send_message(chat_id = admin, text=item['StuID'] + result) # 打卡结果打印

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
    result = NotionDatabase.DataBase_additem(DATABASEID, body, StuID)
    if (person == admin):
        result = "用户更新：" + result
    context.bot.send_message(chat_id=person, text=result) # 打卡结果打印

checktime = '00:59'
def check(update, context): # 添加自动打卡
    if (len(context.args) == 2): # /check 后面必须是两个参数
        message = (
            f"欢迎使用自动打卡功能~\n\n"
            f"将在每日{checktime}打卡\n\n"
            f"请稍等哦，正在给您的信息添加到数据库~\n\n"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)
        adddata(update.effective_chat.id, context, context.args[0], context.args[1], "**", '1', update.effective_chat.id)
    else:
        message = (
            f"格式错误哦\~，需要两个参数，注意学号用户名之间的空格\n\n"
            f"请输入 `/check 学号 教务处密码`\n\n"
            f"例如学号为 123，密码是 123\n\n"
            f"则输入 `/check 123 123`\n\n"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='MarkdownV2')

def inuaa(update, context): # 当用户输入/inuaa 学号，密码 时，自动打卡，调用nuaa.py文件
    if (len(context.args) == 2): # /inuaa后面必须是两个参数
        context.bot.send_message(chat_id=update.effective_chat.id, text="请稍等哦，大约20秒就好啦~")
        result = "test"
        # cookies = ''
        # delay = 6
        # login_id = context.args[0]
        # login_password = context.args[1]
        # for _ in range(2):
        #     try:
        #         time.sleep(delay)
        #         r = requests.get('https://m.nuaa.edu.cn/uc/wap/login', cookies=cookies)
        #         print('get login page:', r.status_code)
        #         print('1')
        #         cookies = dict(r.cookies)
        #         print('2')
        #         # print(r.cookies)
        #         time.sleep(delay)
        #         print('start check')
        #         r = requests.get('https://m.nuaa.edu.cn/uc/wap/login/check', cookies=cookies, data='username={}&password={}'.format(login_id, login_password))
        #         print('login...:', r.status_code)
        #         if ("账户或密码错误" in r.text):
        #             return "账户或密码错误", '', ''
        #         cookies.update(dict(r.cookies))
        #         # headers['Cookie'] = cookie
        #         for _ in range(2):
        #             try:
        #                 time.sleep(delay)
        #                 response = requests.get('https://m.nuaa.edu.cn/ncov/wap/default', cookies=cookies)
        #                 response.encoding = 'utf-8'
        #                 print(response.text)
        #                 uid = re.search(r'"uid":"([0-9]*)"', response.text).group(1)
        #                 id = re.search(r'"id":([0-9]*)', response.text).group(1)
        #                 # print(uid, id)
        #                 # return uid,id
        #             except Exception as e:
        #                 print(e)
        #         # uid, id = get_uid_id(cookies)
        #         # return cookies, uid, id
        #     except Exception as e:
        #         print(e)
        #         print('login failed.')
        #         pass
        # if ("账户或密码错误" in cookies):
        #     print("{{(>_<)}}}，账户或密码错误，呜呜呜。")
        # else:
        #     print("登录成功！")

        cookies = ''
        r = requests.get('https://m.nuaa.edu.cn/uc/wap/login', cookies=cookies)
        print('get login page:', r.status_code)
        r = requests.get('https://m.nuaa.edu.cn/uc/wap/login/check', cookies=cookies)
        print('get login page:', r.status_code)
        r = requests.get('https://m.nuaa.edu.cn/ncov/wap/default', cookies=cookies)
        print('get login page:', r.status_code)
        # result = startinuaa(context.args[0], context.args[1]) # 调用打卡程序
        context.bot.send_message(chat_id=update.effective_chat.id, text="完成调用打卡函数")
        context.bot.send_message(chat_id=update.effective_chat.id, text=result) # 打卡结果打印
        context.bot.send_message(chat_id=admin, text=context.args[0] + result) # 打卡结果打印
        adddata(admin, context, context.args[0], "*", "**", '0', update.effective_chat.id)
    else:
        message = (
            f"格式错误哦\~，需要两个参数，注意学号用户名之间的空格\n\n"
            f"请输入 `/inuaa 学号 教务处密码`\n\n"
            f"例如学号为 123，密码是 123\n\n"
            f"则输入 `/inuaa 123 123`\n\n"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='MarkdownV2')

def get_dispatcher(bot):
    """Create and return dispatcher instances"""
    dispatcher = Dispatcher(bot, None, workers=0)

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("check", check))
    dispatcher.add_handler(CommandHandler("inuaa", inuaa))
    dispatcher.add_handler(CommandHandler("dailysign", daily))
    dispatcher.add_handler(CallbackQueryHandler(button_press))

    return dispatcher
