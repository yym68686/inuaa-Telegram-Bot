#!/bin/bash
git clone --depth 1 https://github.com/yym68686/inuaa-Telegram-Bot.git > /dev/null
echo "code downloaded..." >> /bot/log 2>&1
cd inuaa-Telegram-Bot
touch /bot/log
nohup python -u /bot/inuaa-Telegram-Bot/webhook.py >> /bot/log 2>&1 &
echo "web is starting..." >> /bot/log 2>&1
tail -f /bot/log