# telegram bot NUAA i南航 自动打卡机器人

- 使用无服务，部署在<https://vercel.com>，在 https://github.com/odysseusmax/calculator-bot 基础上修改的。

- 在 telegram 搜索 [@yym68686bot](https://t.me/yym68686bot)

- 轻量级数据库，不考虑性能，直接用Notion的Database做了数据库

# 上手指南

https://yym68686.top/TelegramBot

# Calculator Bot

原项目的功能是一个计算器机器人，本项目保留了这个功能，说不定未来会用到。

## Steps

### 在 vercel 添加环境变量

- Add your telegram bot token as `BOT_TOKEN` variable
- 把 notion 的 token 作为 NotionToken 变量
- 数据库的 pageid 作为 DATABASEID 变量

### Register webhook

```bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://your-project-name.vercel.app/api/webhook/"
```
