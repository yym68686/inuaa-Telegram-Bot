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

使用机器人，在 telegram 搜索 [@yym68686bot](tg://resolve?domain=yym68686bot)

轻量级数据库，不考虑性能，直接用 Notion 的 Database 做了数据库

- main 分支    fly.io 部署实例
- heroku 分支 HeroKu 部署实例
- vercel 分支  vercel 部署实例
- action 分支 定时打卡任务
- argo 分支   内网通过 Cloudflare Argo Tunnel 内网穿透实例

# telegram bot 部署到 fly.io

## Docker

dockerfile

```

```



## References

[python-telegram-bot v13 webhook 文档](https://github.com/python-telegram-bot/v13.x-wiki/wiki/Webhooks)

[python-telegram-bot Transition guide to Version 12.0](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Transition-guide-to-Version-12.0#handler-callbacks)

[Telegram Bot API](https://core.telegram.org/bots/api)

## Steps

- 添加 telegram bot token 作为 BOT_TOKEN 变量
- 把 notion 的 token 作为 NotionToken 变量
- 数据库的 pageid 作为 DATABASEID 变量

