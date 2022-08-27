# git add . && git commit -m "modify main.py" && git push origin main
# heroku logs --tail -a yymtg
import os
import NotionDatabase
from nuaa import startinuaa
import logging, datetime, pytz
from telegram import Update
from telegram.ext import Updater, CallbackContext

TOKEN = os.getenv("TOKEN") # 从环境变量自动获取telegram bot Token
DATABASEID = os.getenv("DATABASEID")
checktime = '00:59'

admin = 917527833

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

def weather(update, context):
    context.job_queue.run_daily(msg, datetime.time(hour=1, minute=56, tzinfo=pytz.timezone('Asia/Shanghai')), days=(0, 1, 2, 3, 4, 5, 6), context=admin)

if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True)
    dailysign()