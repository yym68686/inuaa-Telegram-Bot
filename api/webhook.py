import os
import time
import logging
import schedule
from flask import Flask, Blueprint, request, jsonify
from telegram import Bot, Update

from bot import get_dispatcher, dailysign
from config import checktime, BOT_TOKEN

app = Flask(__name__)
api = Blueprint("serverless_handler", __name__)
bot = Bot(BOT_TOKEN)
app.config["tg_bot"] = bot
app.config["tg_dispatcher"] = get_dispatcher(bot)
logger = logging.getLogger(__name__)


@api.route("/", methods=["POST"])
def webhook():
    update_json = request.get_json()
    logger.info("input to function %s", update_json)
    update = Update.de_json(update_json, app.config["tg_bot"])
    app.config["tg_dispatcher"].process_update(update)
    return jsonify({"status": "ok"})


@api.route("/")
def home():
    return "Hi there"


app.register_blueprint(api, url_prefix="/api/webhook")

# def toUTC(t):
#     t2 = int(t[:2])
#     if t2 - 8 < 0:
#         t2 += 24
#     t2 -= 8
#     t = str(t2) + t[2:]
#     if len(t) == 4:
#         t = "0" + t
#     return t

# schedule.every().day.at(toUTC(checktime)).do(dailysign)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
