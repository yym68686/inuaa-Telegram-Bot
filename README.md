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

setup.sh

```bash
#!/bin/bash
git clone --depth 1 https://github.com/yym68686/inuaa-Telegram-Bot.git > /dev/null
echo "code downloaded..." >> /home/log 2>&1
cd inuaa-Telegram-Bot
touch /home/log
nohup python -u /home/inuaa-Telegram-Bot/webhook.py >> /home/log 2>&1 &
echo "web is starting..." >> /home/log 2>&1
tail -f /home/log
```

dockerfile

```dockerfile
FROM python:3.9.15-slim-bullseye
WORKDIR /home
EXPOSE 8080
COPY ./setup.sh /
COPY ./requirements.txt /
RUN apt-get update && apt -y install git \
    ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r /requirements.txt \
    && pyppeteer-install
ENTRYPOINT ["/setup.sh"]
```

构建

```bash
docker build -t bot:1.0 --platform linux/amd64 .
```

运行

```bash
docker exec -it $(docker run -p 8080:8080 -dit \
-e BOT_TOKEN="5569***********FybvZJOmGrST_w" \
-e DATABASEID="e50db3e******017d71e60dee6" \
-e NotionToken="secret***********g5ltrxL3thq6qdPkKyywqZN" \
-e URL="https://test.com/" \
-e MODE="prod" \
bot:1.0) bash
```

- 添加 telegram bot token 作为 BOT_TOKEN 变量
- 把 notion 的 token 作为 NotionToken 变量
- Notion database 数据库的 pageid 作为 DATABASEID 变量
- URL 是 bot 的 webhook 地址
- MODE 设置生产环境 prod

关闭所有容器

```bash
docker rm -f $(docker ps -aq)
```

查看 pyppeteer 日志

```python
from pyppeteer.launcher import Launcher
' '.join(Launcher().cmd)
```

把输出的命令放到终端里。

## References

[修复 Failed to parse the contents of /proc/self/maps](Failed to parse the contents of /proc/self/maps)
