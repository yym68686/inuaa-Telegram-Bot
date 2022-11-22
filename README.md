```

 ███╗   ██╗  ██████╗      ██╗    ██╗  █████╗  ██╗      ██╗      ███████╗ ██╗   
 ████╗  ██║ ██╔═══██╗     ██║    ██║ ██╔══██╗ ██║      ██║      ██╔════╝ ██║   
 ██╔██╗ ██║ ██║   ██║     ██║ █╗ ██║ ███████║ ██║      ██║      ███████╗ ██║   
 ██║╚██╗██║ ██║   ██║     ██║███╗██║ ██╔══██║ ██║      ██║      ╚════██║ ╚═╝   
 ██║ ╚████║ ╚██████╔╝     ╚███╔███╔╝ ██║  ██║ ███████╗ ███████╗ ███████║ ██╗   
 ╚═╝  ╚═══╝  ╚═════╝       ╚══╝╚══╝  ╚═╝  ╚═╝ ╚══════╝ ╚══════╝ ╚══════╝ ╚═╝
```

# telegram bot NUAA i南航 自动打卡 自助申请出校机器人

好的大学没有围墙！

在 telegram 搜索 [@yym68686bot](tg://resolve?domain=yym68686bot) 使用机器人。

轻量级数据库，不考虑性能，直接用 Notion 的 Database 做了数据库

- main 分支    fly.io 部署实例
- heroku 分支 HeroKu 部署实例
- vercel 分支  vercel 部署实例
- action 分支 定时打卡任务
- argo 分支   内网通过 Cloudflare Argo Tunnel 内网穿透实例

# telegram bot 部署到 fly.io

## Docker

sh

```bash
#!/bin/bash
git clone https://github.com/yym68686/inuaa-Telegram-Bot.git
cd inuaa-Telegram-Bot
touch /home/log
nohup python -u /home/inuaa-Telegram-Bot/webhook.py >> /home/log 2>&1 &
tail -f /home/log
```

dockerfile

```dockerfile
FROM ubuntu:20.04
WORKDIR /home
RUN apt-get update && apt -y install git

```

构建

```bash
docker build --network=host -t bot:1.0 .
```

运行

```bash

```

关闭所有容器

```bash
docker rm -f $(docker ps -aq)
```

- buster:Debian 10
- stretch:Debian 9
- jessie:Debian 8

```python
from pyppeteer.launcher import Launcher
' '.join(Launcher().cmd)
```

## References

[python-telegram-bot v13 webhook 文档](https://github.com/python-telegram-bot/v13.x-wiki/wiki/Webhooks)

[python-telegram-bot Transition guide to Version 12.0](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Transition-guide-to-Version-12.0#handler-callbacks)

[Telegram Bot API](https://core.telegram.org/bots/api)

## Steps

- 添加 telegram bot token 作为 BOT_TOKEN 变量
- 把 notion 的 token 作为 NotionToken 变量
- 数据库的 pageid 作为 DATABASEID 变量
