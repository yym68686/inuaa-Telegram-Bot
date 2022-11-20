import telegram
from bot import setup
from flask import Flask, request

URL = "https://test.com/"
BOT_TOKEN = "5569497961:AA**********JOmGrST_w"
PORT = 8080

app = Flask(__name__)
updater, dispatcher = setup(BOT_TOKEN)

@app.route('/', methods=['GET'])
def hello():
    return 'hello world!'

@app.route('/{}'.format(BOT_TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), updater.bot)
    dispatcher.process_update(update)
    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = updater.bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=BOT_TOKEN))
    if s:
        return "webhook ok"
    else:
        return "webhook failed"

if __name__ == '__main__':
    print(set_webhook())
    app.run(host='127.0.0.1', port=PORT, debug=True)