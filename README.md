# telegram bot 利用 Cloudflare Argo Tunnel 做 webhook 内网穿透

Cloudflare Argo Tunnel 是一种 frp 服务，但省去了配置服务器的烦恼，利用 Cloudflare 部署的全球节点能力，快速将内网服务穿透到公网中。本文利用 Cloudflare Argo Tunnel 内网穿透服务做 Telegram bot 的 webhook。

在内网将 telegram bot 与 flask 结合起来，flask 负责解析 json 消息包，同时跟 telegram api 沟通，设置机器人的 webhook 地址。当用户发消息给他的客户端的时候，客户端发送消息给 telegram 服务器，telegram 服务器向机器人中我们提前设置好的 webhook 地址发送消息包，Cloudflare 接收到 telegram 服务器发来的消息包，转发给内网的 telegram bot，消息包首先被 flask 拦截解析 json 数据给机器人，机器人再进一步处理再发给用户。

Cloudflare Argo Tunnel 使用方法见我的 [wiki](https://wiki.yym68686.top/tools/CloudFlare)

创建管道并绑定域名

```bash
cloudflared tunnel create bot
cloudflared tunnel route dns bot test.com
```

~/.cloudflared/config.yml 配置

```yaml
tunnel: 2dfba3db-b87c-4d4b-a9ce-da03bcfd98a4
credentials-file: /Users/username/.cloudflared/2dfba3db-b87c-4d4b-a9ce-da03bcfd98a4.json
protocol: http2

ingress:
  - hostname: test.com
    service: http://127.0.0.1:8080
  - service: http_status:404
```

运行 Cloudflare Argo Tunnel

```bash
cloudflared --config ～/.cloudflared/config.yml tunnel run bot
```

在机器人项目目录下执行

```bash
python webhook.py
```

开启 flask Debug 环境，终端执行

```bash
export FLASK_DEBUG=True
```

查看机器人 webhook 链接是否生效，浏览器访问

```
https://api.telegram.org/bot<bot-token>/getWebhookInfo
```

## References

[python-telegram-bot v13 webhook 文档](https://github.com/python-telegram-bot/v13.x-wiki/wiki/Webhooks)

[python-telegram-bot Transition guide to Version 12.0](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Transition-guide-to-Version-12.0#handler-callbacks)

[Telegram Bot API](https://core.telegram.org/bots/api)



