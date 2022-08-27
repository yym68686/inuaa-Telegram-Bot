# git add . && git commit -m "modify main.py" && git push origin $(git rev-parse --abbrev-ref HEAD)
import os
import NotionDatabase
from nuaa import startinuaa
from telegram.ext import Updater

TOKEN = os.getenv("TOKEN") # 从环境变量自动获取telegram bot Token
DATABASEID = os.getenv("DATABASEID")
checktime = '00:59'
admin = 917527833

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

if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True)
    dailysign()