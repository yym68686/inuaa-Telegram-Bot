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

- main 分支 HeroKu 部署实例
- vercel 分支 vercel 部署实例
- action 分支定时打卡任务

本文 Blog 地址：[https://yym68686.top/TelegramBot](https://yym68686.top/TelegramBot)

> 处于安全性考虑，本机器人不保存密码（听说有人搞这个被开除了）。这意味着你需要每天给机器人投喂命令இ௰இ，他才能打卡。

# 背景

很早就想写个telegram机器人了，上次写telegram bot还是去年用js写的，调用图灵机器人的api。但这个聊天机器人也太拉了吧。。免费版本一天只有几次请求次数，最后telegram机器人折腾计划就搁置了。昨天我还在想学校健康打卡，为什么会有这么形式主义的东西。一个合格的码农怎么能屈服于这种事情。于是又开始折腾tg bot了，我保证写完这个就去学习/(ㄒoㄒ)/~~。这个机器人一言以蔽之就是一个《缝合怪》，不过属实让我惊叹于telegram bot定制化程度。首先给个机器人名字@yym68686bot，直接在telegram搜索就行啦。

项目地址：

[https://github.com/yym68686/tgbot](https://github.com/yym68686/tgbot)

# HeroKu 环境配置

具体思路就是python写逻辑代码，push到HeroKu自动部署机器人。

首先我找到了这篇文章：

[Telegram 机器人程序开发](https://lijingcheng.github.io/posts/telegram-bot/)

第一次知道了HeroKu自动化部署。但文章缺乏一些细节，也踩了不少坑。

HeroKu官网：

[Heroku](https://dashboard.heroku.com/)

先在HeroKu平台创建一个账号，添加一个app，不过最近不能直接与github仓库关联，因为：

[Heroku Status](https://status.heroku.com/incidents/2413)

关联github仓库后，github仓库push后，HeroKu会自动在他的服务器上构建好应用，项目自动化部署完成，还挺香的。

这里我们换一种提交仓库的方式，在app→Deploy→Deployment method→Heroku Git，在

[The Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

下载HeroKu CLI工具，在本地安装完后，添加环境变量。在终端登录HeroKu：

```python
heroku login -i
```

密码是一个token，这里获取：

[Heroku](https://dashboard.heroku.com/account/applications)

如果要创建app，输入：

```python
heroku apps:create name
```

查看已创建的 app

```python
heroku apps
```

查看app信息

```python
heroku apps:info <appname>
```

因为要push到HeroKu仓库，需要添加远程主机：

```python
git remote add heroku <https://git.heroku.com/yymtg.git>
```

# 编写bot代码

## 环境准备

在目录下创建必要的文件：

```python
E:\\CODE\\TGBOT
│  main.py          # bot 主程序
│  nuaa.py          # 打卡脚本
│  Procfile         # HeroKu通过识别这个文件，运行主程序 
│  README.md
│  requirements.txt # 必要的python包，包含版本信息，HeroKu自动安装
│  runtime.txt      # python版本信息
```

根据telegram bot api集成工具：

[GitHub - python-telegram-bot/python-telegram-bot: We have made you a wrapper you can&#39;t refuse](https://github.com/python-telegram-bot/python-telegram-bot)

python版本大于3.6.8。请自行创建虚拟环境。

先安装telegram bot api集成软件包：

```python
pip install python-telegram-bot requests
```

打卡需要requests，一并安装上去。

导出软件包环境：

```python
python -m pip freeze > requirements.txt
```

## Procfile内容

```python
web: python main.py
```

## runtime.txt内容

```python
python-3.9.12
```

## [main.py](http://main.py) bot主程序

```python
import os
import sys
import logging
from nuaa import startinuaa
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.getenv("TOKEN") # 从环境变量自动获取telegram bot Token
MODE = os.getenv("MODE")
PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def start(update, context): # 当用户输入/start时，返回文本
    update.message.reply_text('欢迎使用 🎉')

def help(update, context):
    update.message.reply_text('我是人见人爱的yym的小跟班~')

def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def unknown(update: Update, context: CallbackContext): # 当用户输入未知命令时，返回文本
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def caps(update: Update, context: CallbackContext): # 小的测试功能，也是官方示例，将用户参数转化为大写
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def inuaa(update: Update, context: CallbackContext): # 当用户输入/inuaa 学号，密码 时，自动打卡，调用nuaa.py文件
    if (len(context.args) == 2): # /inuaa后面必须是两个参数
        context.bot.send_message(chat_id=update.effective_chat.id, text="请稍等哦，大约20秒就好啦~")
        result = startinuaa(context.args[0], context.args[1]) # 调用打卡程序
        context.bot.send_message(chat_id=update.effective_chat.id, text=result) # 打卡结果打印
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="格式错误哦~，请输入 /inuaa [学号] [教务处密码]")

if __name__ == '__main__':
    if MODE == "dev": # 本地调试，需要挂代理，这里使用的是Clash
        updater = Updater(TOKEN, use_context=True, request_kwargs={
            'proxy_url': '<https://127.0.0.1:7890>' # 需要代理才能使用 telegram
        })
    elif MODE == "prod": # 生产服务器在美国，不需要代理
        updater = Updater(TOKEN, use_context=True)
    else:
        logger.error("需要设置 MODE!")
        sys.exit(1)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("caps", caps))
    dispatcher.add_handler(CommandHandler("inuaa", inuaa)) # 当用户输入/inuaa时，调用inuaa()函数

    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_error_handler(error)

    if MODE == "dev": # 本地调试
        updater.start_polling()
    elif MODE == "prod": # HeroKu 远程生产环境
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    updater.idle()
```

TOKEN和MODE和HEROKU_APP_NAME变量都是从环境变量获取的，在apps→Settings→Config Vars→Reveal Config Vars里，添加环境变量。机器人的TOKEN可以在BotFather那里获取。MODE规定是本地开发还是生产环境。请务必设置为prod。HEROKU_APP_NAM就是app的名字。

本地调试可以把MODE改为dev，token直接写到脚本里，然后在本地控制台运行：

```bash
python -u main.py
```

在任意聊天窗口发送“ **@userinfobot** ”然后点击这条消息即可打开与**userinfobot**的聊天，发送任意消息给**userinfobot**它会返回你的信息，其中包含一个ID，这就是我们需要的**chat_id.**

## nuaa.py打卡脚本

代码来源：

[GitHub - Wood1314/inuaa](https://github.com/Wood1314/inuaa)

如果想要自行搭建每天自动打卡，可以参考一下这个项目。一顿魔改后：

```python
# -*- coding: UTF-8 -*-

import requests
import time
# import json
import sys
import re
# from send_mail import send_mail

# 如果发包过快会造成502，如果给多个同学打卡请注意一下请求速度
try_times = 2

# 每次requests请求的延迟(s秒)，太低会封IP
delay = 3

'''
教务处的垃圾命名规则
info: {
                sfzhux: 0,
                zhuxdz: '',
                szgj: '',
                szcs: '',
                szgjcs: '',
                sfjwfh: 0,
                sfyjsjwfh: 0,
                sfjcjwfh: 0,
                sflznjcjwfh: 0,
                sflqjkm: '0',
                jkmys: 0,
                sfjtgfxdq: 0,
                nuaaxgymjzqk:"1",  //新冠疫苗接种情况：
                dyzjzsj:"", //第一针接种时间
                bfhzjyq:"3", //不符合接种要求
                hxyxjzap:"2", //后续意向接种安排
                yjzjsj:"", //预计接种时间
                sftjlkjc: '',
                lkjctlsj: '',
                sfsylkjcss: '',
                gjzsftjlkjc: '',
                gjzlkjctlsj: '',
                gjzsfsylkjcss: '',
                ifhxjc:'', //你是否进行了核酸检测
                hsjconetime:"", //第一次检测时间
                hsjconeplace:"", //第一次检测地点
                hsjconejg:"", //第一次检测结果（1/2/3）
                hsjctwotime:"", //第二次检测时间
                hsjctwoplace:"", //第二次检测地点
                hsjctwojg:"", //第二次检测结果（1/2/3）
                hsjcthreetime:"", //第三次检测时间
                hsjcthreeplace:"", //第三次检测地点
                hsjcthreejg:"", //第三次检测结果（1/2/3）
                hsjcfourtime:"", //第四次检测时间
                    hsjcfourplace:"", //第四次检测地点
                    hsjcfourjg:"", //第四次检测结果（1/2/3）
                    ywchxjctime:"",  //已完成核酸检测次数
                hsjclist:"{}",
                // 新增2
                njrddz:"", //您的今日住址（详细到门牌号、宿舍号）
                gzczxq:"", //工作常驻校区(1,2,3)
                ifznqgfxljs:"",  //7月10日后是否有江宁区中高风险地区旅居史
                iflsqgfxljs:"",  //7月10日后是否有溧水区中高风险地区旅居史
                // ifjrglkjc:"", //7月10日以来是否进入过禄口机场大厅或与机场工作人员有密切接触
                // gtjjsfhm:"", //共同居住人员中是否有黄码或7月10日以来经停机场人员
                // ywchscs:"",  //已完成核酸检测次数
                // gtjzsfhzl:"",  //共同居住人是否已黄码转绿或已解除14天隔离观察
                // sffhddjjgc:"",//是否符合单独居家观察条件（与共同居住人用餐等不交叉）
                // end
                // 新增3
                // ifjgzgfxq:"", //7月10日后是否经过除禄口机场外其他中高风险区
                // jgzgfxrq:"",  //7月10日后最后一次经过中高风险区的日期
                // jgzgfxdq:"",  //7月10日后最后一次经过中高风险区的地区
                //  jgzgfxxxdz:"", //7月10日后最后一次经过中高风险区的详细地址
                 zrwjtw:"",  //昨日晚间体温范围
                 jrzjtw:"", //今日早间体温范围
                 jrlvymjrq:"", //7月10日后最后一次进入过禄口机场大厅或与机场工作人员有密切接触的日期
                 ifcyglq:"", //是否处于隔离期/医学观察期
                // end
                // 新增4
                // newwchsjccs:"",  //替换以前的已完成核酸检测次数
                // dsdecjcsj:"", //倒数第二次核酸检测时间
                // dsdechsjcjgtype:"", //倒数第二次核酸检测地点
                // dsdrchsjcdd:"",  //倒数第二次核酸检测地点
            
                // dsdechsjcjg:"",  //倒数第二次核酸检测结果
                // zhyccjcsj:"", //最后一次核酸检测时间
                // zhycchsjcjgtype:"", //最后一次核酸检测地点
                // zhycchsjcdd:"",  //最后一次核酸检测地点
            
                // zhycchsjcjg:"",  //最后一次核酸检测结果
                wskmyy:"",//请简要说明无苏康码原因
                zhycjgdqifjn:"",//7月10日后最后一次经过中高风险区的地区为中国境内还是中国境外

                dqsfzgfxszqs:"", //当前是否在中高风险地区所在设区市（直辖市为区、县）
                gqsfyzgfxljs:"", //过去21天内是否有中高风险区旅居史（不含交通工具经停）
                gqsfyqzfhryjc:"",//过去21天内是否与确诊/疑似病例/无症状感染者/从中高风险区返回人员（已解除隔离观察的不算）有密切接触
                sfyjwljqyhg:"",//28天内是否有境外旅居史且已经回国

                cjfxsfhs:"", //2022年春季返校后是否已做核酸检测
                bzxyy:"", //不在校原因  1-4
                bzxyydesc:"", //不在校原因其他时候的时候
}
'''

def get_uid_id(cookies):
    '''
    获取id与uid
    '''
    for _ in range(try_times):
        try:
            time.sleep(delay)
            response = requests.get(
                '<https://m.nuaa.edu.cn/ncov/wap/default>', cookies=cookies)
            response.encoding = 'utf-8'

            # print(response.text)

            uid = re.search(r'"uid":"([0-9]*)"', response.text).group(1)
            id = re.search(r'"id":([0-9]*)', response.text).group(1)
            print(uid, id)
            return uid,id
        except Exception as e:
            print(e)
    # 就这样吧，让他崩溃，万一假打卡了就不好了
    print('获取id、uid失败')
    return False, '获取id、uid失败\\n'

def login(login_id, login_password):
    '''
    登陆I南航，返回Cookie，失败返回空串
    '''
    # headers['Cookie'] = ''
    cookies = ''
    for _ in range(try_times):
        try:
            time.sleep(delay)
            r = requests.get(
                '<https://m.nuaa.edu.cn/uc/wap/login>', cookies=cookies)
            print('get login page:', r.status_code)
       
            cookies = dict(r.cookies)
            # print(r.cookies)

            time.sleep(delay)
            r = requests.get('<https://m.nuaa.edu.cn/uc/wap/login/check>', cookies=cookies, data='username={}&password={}'.format(login_id, login_password))
            print('login...:', r.status_code)
            if ("账户或密码错误" in r.text):
                return "账户或密码错误", '', ''
            cookies.update(dict(r.cookies))

            # headers['Cookie'] = cookie
            uid, id = get_uid_id(cookies)
            return cookies, uid, id
        except Exception as e:
            print(e)
            print('login failed.')
            pass
    # raise Exception('lOGIN FAIL')
    return '', '', ''

def sign(user):

    '''
    签到，并且发送邮件提醒，成功返回True，失败返回False
    '''
    for _ in range(try_times):
        try:
            data = {
                'sfzhux': '0',
                'zhuxdz': '',
                'szgj': '',
                'szcs': '',
                'szgjcs': '',
                'sfjwfh': '0',
                'sfyjsjwfh': '0',
                'sfjcjwfh': '0',
                'sflznjcjwfh': '0',
                'sflqjkm': '4',
                'jkmys': '1',
                'sfjtgfxdq': '0',
                'tw': '2',
                'sfcxtz': '0',
                'sfjcbh': '0',
                'sfcxzysx': '0',
                'qksm': '',
                'sfyyjc': '0',
                'jcjgqr': '0',
                'remark': '',
                'address': '江苏省南京市江宁区秣陵街道慧园路南京航空航天大学将军路校区',
                'geo_api_info': {"type":"complete","position":{"Q":31.939607,"R":118.791155,"lng":118.791155,"lat":31.939607},"location_type":"html5","message":"Get geolocation success.Don't need convert.Get address success.","accuracy":29,"isConverted":1,"status":1,"addressComponent":{"citycode":"025","adcode":"320115","businessAreas":[{"name":"开发区","id":"320115","location":{"Q":31.925973,"R":118.80980399999999,"lng":118.809804,"lat":31.925973}}],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"将军大道","streetNumber":"29号","country":"中国","province":"江苏省","city":"南京市","district":"江宁区","towncode":"320115011000","township":"秣陵街道"},"formattedAddress":"江苏省南京市江宁区秣陵街道慧园路南京航空航天大学将军路校区","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"},
                'area': '江苏省 南京市 江宁区',
                'province': '江苏省',
                'city': '南京市',
                'sfzx': '0',
                'sfjcwhry': '0',
                'sfjchbry': '0',
                'sfcyglq': '0',
                'gllx': '',
                'glksrq': '',
                'jcbhlx': '',
                'jcbhrq': '',
                'bztcyy': '',
                'sftjhb': '0',
                'sftjwh': '0',
                'sftjwz': '0',
                'sfjcwzry': '0',
                'jcjg': '',
                'date': time.strftime("%Y%m%d", time.localtime()),  # 打卡年月日一共8位
                'uid': user['uid'],  # UID
                'created': round(time.time()), # 时间戳
                'jcqzrq': '',
                'sfjcqz': '',
                'szsqsfybl': '0',
                'sfsqhzjkk': '0',
                'sqhzjkkys': '',
                'sfygtjzzfj': '0',
                'gtjzzfjsj': '',
                'created_uid': '0',
                'id': user['id'],# 打卡的ID，其实这个没影响的
                'gwszdd': '',
                'sfyqjzgc': '',
                'jrsfqzys': '',
                'jrsfqzfy': '',
                'ismoved': '0',
                'dqsfzgfxszqs':'0', #当前是否在低风险地区
                'bfhzjyq': '3', #不符合接种要求
                'cjfxsfhs': '1', #春季返校后是否坐核酸
                'gzczxq': '2', #工作常驻校区
                'sfjkyc': '0',
                'sfmrhs': '1',
                'ifcyglq': '0',
                'cjfxsfhs': '1',
            }
            time.sleep(delay)
            r = requests.post('<https://m.nuaa.edu.cn/ncov/wap/default/save>', data=data, cookies=user['cookie'])
            print('sign statue code:', r.status_code)
            print('sign return:', r.text)
            r.encoding = 'utf-8'
        
            if r.text.find('成功') >= 0:
                print('打卡成功')
                return True
            else:
                print('打卡失败，尝试重新登陆')
                user['cookie'] = login(user['studentid'], user['password'])
        except Exception as e:
            print('尝试失败')
            print(e)
            pass
    return False

def startinuaa(studentid, password):
    user = {}
    user['studentid'] = studentid
    user['password'] = password
    if (studentid != '' and password != ''):
        user['cookie'], user['uid'], user['id'] = login(studentid, password)
        if ("账户或密码错误" in user['cookie']):
                return "{{(>_<)}}}，账户或密码错误，呜呜呜。"
        if sign(user):
            return "打卡成功！"
        else:
            return "打卡失败！"
    else:
        return "输入格式错误！"

if __name__ == '__main__':
    startinuaa(sys.argv[1], sys.argv[2])
```

将本地main分支推送到HeroKu远程master分支

```python
git push heroku main:master
```

如果本地分支和远端分支一样则：

```python
git push heroku master
```

也可以用这个命令提交，同时push到github：

```python
cd C:\\Users\\15497\\Desktop\\tgbot && git add . && git commit -m "add Automatic clock in" && git push heroku main:master && git push origin main
```

如果出了问题想要调试，可以使用命令查看日志：

```python
heroku logs --tail -a <appname>
```

## 最后一步

在HeroKu网站的app内的Resources里，把 `web python main.py`右边的开关开下来。然后就可以在 telegram 里给机器人发消息啦。

# 定时任务

vercel 无服务并不能实现自动打卡，HeroKu Scheduler 需要付费，脚本内使用 import schedule 也不可行，HeroKu 会自动暂停服务，知道下次用户用 WebHook 自动唤醒。所以只能用 Github Actions 实现。

# 自动申请出校

自助申请，自己审批，摆脱辅导员！

好的大学没有围墙！

用 BurpSuite 抓包，然后用 HackRequests 模块重放 POST 请求。

解决 pyppeteer Browser closed unexpectedly

[https://stackoverflow.com/a/70074296](https://stackoverflow.com/a/70074296)

HeroKu 利用 chorme 环境使用 pyppeteer 无头服务器模式获取用户 cookies，把下面两个包加入 HeroKu -> Setting -> Buildpacks

[jontewks/heroku-buildpack-puppeteer-firefox (github.com)](https://github.com/jontewks/heroku-buildpack-puppeteer-firefox)

[https://github.com/heroku/heroku-buildpack-google-chrome](https://github.com/heroku/heroku-buildpack-google-chrome)

# TODO

* [ ] 编写通用 POST 请求

两个 POST 对比：

[From UNIX Timestamp, 4 more - CyberChef (gchq.github.io)](https://gchq.github.io/CyberChef/#recipe=From_UNIX_Timestamp('Seconds%20(s)'/disabled)To_UNIX_Timestamp('Seconds%20(s)',true,true/disabled)URL_Decode()Diff('%5C%5Cn%5C%5Cn','Character',true,true,false,false)JSON_Beautify('%20%20%20%20',false,true/disabled)&input=JTdCJTIyX1ZBUl9FWEVDVVRFX0lOREVQX09SR0FOSVpFX05hbWUlMjIlM0ElMjIlRTUlQkMlQTAlRTQlQjglODklRTUlQUQlQTYlRTklOTklQTIlMjIlMkMlMjJfVkFSX0FDVElPTl9JTkRFUF9PUkdBTklaRVNfQ29kZXMlMjIlM0ElMjJ7Nn0lMjIlMkMlMjJfVkFSX0FDVElPTl9SRUFMTkFNRSUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNCVCOCU4OSUyMiUyQyUyMl9WQVJfQUNUSU9OX09SR0FOSVpFJTIyJTNBJTIyezZ9JTIyJTJDJTIyX1ZBUl9FWEVDVVRFX09SR0FOSVpFJTIyJTNBJTIyezZ9JTIyJTJDJTIyX1ZBUl9BQ1RJT05fSU5ERVBfT1JHQU5JWkUlMjIlM0ElMjJ7Nn0lMjIlMkMlMjJfVkFSX0FDVElPTl9JTkRFUF9PUkdBTklaRV9OYW1lJTIyJTNBJTIyJUU1JUJDJUEwJUU0JUI4JTg5JUU1JUFEJUE2JUU5JTk5JUEyJTIyJTJDJTIyX1ZBUl9BQ1RJT05fT1JHQU5JWkVfTmFtZSUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNSVBRCVBNiVFOSU5OSVBMiUyMiUyQyUyMl9WQVJfRVhFQ1VURV9PUkdBTklaRVNfTmFtZXMlMjIlM0ElMjIlRTUlQkMlQTAlRTQlQjglODklRTUlQUQlQTYlRTklOTklQTIlMjIlMkMlMjJfVkFSX09XTkVSX09SR0FOSVpFU19Db2RlcyUyMiUzQSUyMns2fSUyMiUyQyUyMl9WQVJfQUREUiUyMiUzQSUyMjEwLjEwMC4xMTcuMjAlMjIlMkMlMjJfVkFSX09XTkVSX09SR0FOSVpFU19OYW1lcyUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNSVBRCVBNiVFOSU5OSVBMiUyMiUyQyUyMl9WQVJfVVJMJTIyJTNBJTIyaHR0cHMlM0ElMkYlMkZlaGFsbC5udWFhLmVkdS5jbiUyRmluZm9wbHVzJTJGZm9ybSUyRnswfSUyRnJlbmRlciUzRnRoZW1lJTNEbnVhYV9uZXclMjIlMkMlMjJfVkFSX0VYRUNVVEVfT1JHQU5JWkVfTmFtZSUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNSVBRCVBNiVFOSU5OSVBMiUyMiUyQyUyMl9WQVJfUkVMRUFTRSUyMiUzQSUyMnRydWUlMjIlMkMlMjJfVkFSX1RPREFZJTIyJTNBJTIyezV9JTIyJTJDJTIyX1ZBUl9OT1dfTU9OVEglMjIlM0ElMjI5JTIyJTJDJTIyX1ZBUl9BQ1RJT05fVVNFUkNPREVTJTIyJTNBJTIyMTYyMDEwMjE5JTIyJTJDJTIyX1ZBUl9BQ1RJT05fQUNDT1VOVCUyMiUzQSUyMjE2MjAxMDIxOSUyMiUyQyUyMl9WQVJfQUNUSU9OX0lOREVQX09SR0FOSVpFU19OYW1lcyUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNSVBRCVBNiVFOSU5OSVBMiUyMiUyQyUyMl9WQVJfT1dORVJfQUNDT1VOVCUyMiUzQSUyMjE2MjAxMDIxOSUyMiUyQyUyMl9WQVJfQUNUSU9OX09SR0FOSVpFU19OYW1lcyUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNSVBRCVBNiVFOSU5OSVBMiUyMiUyQyUyMl9WQVJfU1RFUF9DT0RFJTIyJTNBJTIyU1FSJTIyJTJDJTIyX1ZBUl9PV05FUl9QSE9ORSUyMiUzQSUyMjEyMzQ1Njc4OTQ1JTIyJTJDJTIyX1ZBUl9PV05FUl9VU0VSQ09ERVMlMjIlM0ElMjIxNjIwMTAyMTklMjIlMkMlMjJfVkFSX0VYRUNVVEVfT1JHQU5JWkVTX0NvZGVzJTIyJTNBJTIyezZ9JTIyJTJDJTIyX1ZBUl9OT1dfREFZJTIyJTNBJTIyMSUyMiUyQyUyMl9WQVJfT1dORVJfUkVBTE5BTUUlMjIlM0ElMjIlRTUlQkMlQTAlRTQlQjglODklRTQlQjglODklMjIlMkMlMjJfVkFSX0VOVFJZX1RBR1MlMjIlM0ElMjIwMS0lRTclOTYlQUIlRTYlODMlODUlRTklOTglQjIlRTYlOEUlQTclRTYlOUMlOEQlRTUlOEElQTElMkMlRTclQTclQkIlRTUlOEElQTglRTclQUIlQUYlMjIlMkMlMjJfVkFSX05PVyUyMiUzQSUyMjE2NjIwMzg4NTclMjIlMkMlMjJfVkFSX1VSTF9BdHRyJTIyJTNBJTIyJTdCJTVDJTIydGhlbWUlNUMlMjIlM0ElNUMlMjJudWFhX25ldyU1QyUyMiU3RCUyMiUyQyUyMl9WQVJfRU5UUllfTlVNQkVSJTIyJTNBJTIyMTMzNTczOTclMjIlMkMlMjJfVkFSX0VYRUNVVEVfSU5ERVBfT1JHQU5JWkVTX05hbWVzJTIyJTNBJTIyJUU1JUJDJUEwJUU0JUI4JTg5JUU1JUFEJUE2JUU5JTk5JUEyJTIyJTJDJTIyX1ZBUl9FTlRSWV9OQU1FJTIyJTNBJTIyXyVFNyU5NiVBQiVFNiU4MyU4NSVFOSU5OCVCMiVFNiU4RSVBNyVFNiU5QyU5RiVFNSVBRCVBNiVFNyU5NCU5RiVFOSU5QiVCNiVFNiU5OCU5RiVFOCVCRiU5QiVFNSU4NyVCQSVFNiVBMCVBMSVFNyU5NCVCMyVFOCVBRiVCNyUyMiUyQyUyMl9WQVJfU1RFUF9OVU1CRVIlMjIlM0ElMjJ7MH0lMjIlMkMlMjJfVkFSX1BPU0lUSU9OUyUyMiUzQSUyMns2fSUzQTExJTNBMTYyMDEwMjE5JTIyJTJDJTIyX1ZBUl9BQ1RJT05fUEhPTkUlMjIlM0ElMjIxMjM0NTY3ODk0NSUyMiUyQyUyMl9WQVJfRVhFQ1VURV9JTkRFUF9PUkdBTklaRVNfQ29kZXMlMjIlM0ElMjJ7Nn0lMjIlMkMlMjJfVkFSX0VYRUNVVEVfUE9TSVRJT05TJTIyJTNBJTIyezZ9JTNBMTElM0ExNjIwMTAyMTklMjIlMkMlMjJfVkFSX0FDVElPTl9PUkdBTklaRVNfQ29kZXMlMjIlM0ElMjJ7Nn0lMjIlMkMlMjJfVkFSX0VYRUNVVEVfSU5ERVBfT1JHQU5JWkUlMjIlM0ElMjJ7Nn0lMjIlMkMlMjJfVkFSX05PV19ZRUFSJTIyJTNBJTIyMjAyMiUyMiUyQyUyMmdyb3VwUVdERExpc3QlMjIlM0ElNUIwJTVEJTJDJTIyZmllbGRITURGWiUyMiUzQSUyMjIlMjIlMkMlMjJmaWVsZFhTU0YlMjIlM0ElMjIlRTYlOUMlQUMlRTclQTclOTElRTclOTQlOUYlMjIlMkMlMjJmaWVsZFNRU0olMjIlM0ExNjYyMDM4ODU3JTJDJTIyZmllbGRBeG0lMjIlM0ElMjIxNjIwMTAyMTklMjIlMkMlMjJmaWVsZEF4bV9OYW1lJTIyJTNBJTIyJUU1JUJDJUEwJUU0JUI4JTg5JUU0JUI4JTg5JTIyJTJDJTIyZmllbGRBeHklMjIlM0ElMjJ7Nn0lMjIlMkMlMjJmaWVsZEF4eV9OYW1lJTIyJTNBJTIyJUU1JUJDJUEwJUU0JUI4JTg5JUU1JUFEJUE2JUU5JTk5JUEyJTIyJTJDJTIyZmllbGRBeGglMjIlM0ElMjIxNjIwMTAyMTklMjIlMkMlMjJmaWVsZEFseGRoJTIyJTNBJTIyMTIzNDU2Nzg5NDUlMjIlMkMlMjJmaWVsZEFmZHklMjIlM0ElMjJ7MX0lMjIlMkMlMjJmaWVsZEFmZHlfTmFtZSUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNCVCOCU4OSUyMiUyQyUyMmZpZWxkRFMlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZERTX05hbWUlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZEFTRlpITSUyMiUzQSUyMjEyMzQ1Njc4OTQ1NjEyMzQ1NiUyMiUyQyUyMmZpZWxkQVNaWFElMjIlM0ElMjIyJTIyJTJDJTIyZmllbGRBU1pYUV9OYW1lJTIyJTNBJTIyJUU1JUIwJTg2JUU1JTg2JTlCJUU4JUI3JUFGJUU2JUEwJUExJUU1JThDJUJBJTIyJTJDJTIyZmllbGRYU0xYJTIyJTNBJTIyJUU0JUJEJThGJUU2JUEwJUExJTIyJTJDJTIyZmllbGRYU0xYX05hbWUlMjIlM0ElMjIlRTQlQkQlOEYlRTYlQTAlQTElMjIlMkMlMjJmaWVsZFNGWUdMUyUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkVFpTRkpLJTIyJTNBJTIyJTIyJTJDJTIyZmllbGRTS00lMjIlM0ElMjIlN0IlNUMlMjJpZCU1QyUyMiUzQSU1QyUyMjE3N2IwOTgzLTlkN2ItNGUwZi1iOWUwLTBkMTVkNjk4NDg4MSU1QyUyMiUyQyU1QyUyMm5hbWUlNUMlMjIlM0ElNUMlMjIxLnBuZyU1QyUyMiUyQyU1QyUyMnNpemUlNUMlMjIlM0ExJTJDJTVDJTIydXJpJTVDJTIyJTNBJTVDJTIyaHR0cHMlM0ElMkYlMkZlaGFsbC5udWFhLmVkdS5jbiUyRmZpbGUlMkYxNzdiMDk4My05ZDdiLTRlMGYtYjllMC0wZDE1ZDY5ODQ4ODElNUMlMjIlMkMlNUMlMjJtaW1lJTVDJTIyJTNBJTVDJTIyaW1hZ2UlMkZwbmclNUMlMjIlN0QlMjIlMkMlMjJmaWVsZFhDTSUyMiUzQSUyMiU3QiU1QyUyMmlkJTVDJTIyJTNBJTVDJTIyNzcyMDQzOGMtY2E5Ni00ZDg0LTgxOGUtZWE0OWE2NWU1NGI2JTVDJTIyJTJDJTVDJTIybmFtZSU1QyUyMiUzQSU1QyUyMjEucG5nJTVDJTIyJTJDJTVDJTIyc2l6ZSU1QyUyMiUzQTElMkMlNUMlMjJ1cmklNUMlMjIlM0ElNUMlMjJodHRwcyUzQSUyRiUyRmVoYWxsLm51YWEuZWR1LmNuJTJGZmlsZSUyRjc3MjA0MzhjLWNhOTYtNGQ4NC04MThlLWVhNDlhNjVlNTRiNiU1QyUyMiUyQyU1QyUyMm1pbWUlNUMlMjIlM0ElNUMlMjJpbWFnZSUyRnBuZyU1QyUyMiU3RCUyMiUyQyUyMmZpZWxkSFNCRyUyMiUzQSUyMiU3QiU1QyUyMmlkJTVDJTIyJTNBJTVDJTIyNjQwMjM1YTItMTYyZS00ZmU1LWExNTYtNWM5YmZjNzg3OGI3JTVDJTIyJTJDJTVDJTIybmFtZSU1QyUyMiUzQSU1QyUyMjEucG5nJTVDJTIyJTJDJTVDJTIyc2l6ZSU1QyUyMiUzQTElMkMlNUMlMjJ1cmklNUMlMjIlM0ElNUMlMjJodHRwcyUzQSUyRiUyRmVoYWxsLm51YWEuZWR1LmNuJTJGZmlsZSUyRjY0MDIzNWEyLTE2MmUtNGZlNS1hMTU2LTVjOWJmYzc4NzhiNyU1QyUyMiUyQyU1QyUyMm1pbWUlNUMlMjIlM0ElNUMlMjJpbWFnZSUyRnBuZyU1QyUyMiU3RCUyMiUyQyUyMmZpZWxkQkxIVFMlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENYUlElMjIlM0F7NX0lMkMlMjJmaWVsZEpTU0olMjIlM0F7NX0lMkMlMjJmaWVsZENYU0pGUk9NJTIyJTNBMCUyQyUyMmZpZWxkQ1hTSlRPJTIyJTNBMCUyQyUyMmZpZWxkQ1hTWSUyMiUzQSUyMi4uLiUyMiUyQyUyMmZpZWxkQ1hMQiUyMiUzQSUyMjElMjIlMkMlMjJmaWVsZEFjeHhjJTIyJTNBJTIyMiUyMiUyQyUyMmZpZWxkQWRzJTIyJTNBJTIyMSUyMiUyQyUyMmZpZWxkQXNoZW5ncyUyMiUzQSU1QiUyMiUyMiU1RCUyQyUyMmZpZWxkQXNoZW5nc19OYW1lJTIyJTNBJTVCJTIyJTIyJTVEJTJDJTIyZmllbGRBc2hpcyUyMiUzQSU1QiUyMiUyMiU1RCUyQyUyMmZpZWxkQXNoaXNfTmFtZSUyMiUzQSU1QiUyMiUyMiU1RCUyQyUyMmZpZWxkQXNoaXNfQXR0ciUyMiUzQSU1QiUyMiU3QiU1QyUyMl9wYXJlbnQlNUMlMjIlM0ElNUMlMjIlNUMlMjIlN0QlMjIlNUQlMkMlMjJmaWVsZEFqdGRkJTIyJTNBJTVCJTIyJTIyJTVEJTJDJTIyZmllbGRDTiUyMiUzQXRydWUlMkMlMjJmaWVsZEFoaWRkZW4lMjIlM0ElMjIlMjIlMkMlMjJmaWVsZEN5ajMlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENzaHIzJTIyJTNBJTIyJTIyJTJDJTIyZmllbGRDc2hyM19OYW1lJTIyJTNBJTIyJTIyJTJDJTIyZmllbGRDc2hkYXRlMyUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkRllaU0glMjIlM0ElMjIlMjIlMkMlMjJmaWVsZEZZWlNIUiUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkRllaU0hSX05hbWUlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZEZZWlNIUlElMjIlM0ElMjIlMjIlMkMlMjJmaWVsZEN5ajQlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENzaHI0JTIyJTNBJTIyJTIyJTJDJTIyZmllbGRDc2hyNF9OYW1lJTIyJTNBJTIyJTIyJTJDJTIyZmllbGRDc2hkYXRlNCUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkQ3lqNSUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkQ3NocjUlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENzaHI1X05hbWUlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENzaHNqNSUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkVE9LRU4lMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENYUlFTVFIlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENYUlFGcm9tJTIyJTNBMTY2MjAzODg1NyUyQyUyMmZpZWxkRlpaRCUyMiUzQSUyMiUyMiU3RCZyZW1hcms9JnJhbmQ9ODUyLjQ4OTc5MDQ5NjcxOCZuZXh0VXNlcnM9JTdCJTIyMiUyQyUyMiUzQSUyMjgzNmM4MjAxLWM5NWUtMTFlOS05MTI3LTAwNTA1NjhhMjgxZiUyMiU3RCZzdGVwSWQ9ezB9JnRpbWVzdGFtcD17Mn0mYm91bmRGaWVsZHM9ZmllbGRDWFNKVE8lMkNmaWVsZEFTWlhRJTJDZmllbGRDWFJRJTJDZmllbGRBc2hlbmdzJTJDZmllbGRBY3h4YyUyQ2ZpZWxkQXhoJTJDZmllbGRGWlpEJTJDZmllbGRDWFJRU1RSJTJDZmllbGRTS00lMkNmaWVsZEF4bSUyQ2ZpZWxkQWx4ZGglMkNmaWVsZENYUlFGcm9tJTJDZmllbGREUyUyQ2ZpZWxkWENNJTJDZmllbGRUT0tFTiUyQ2ZpZWxkWFNMWCUyQ2ZpZWxkU0ZZR0xTJTJDZmllbGRITURGWiUyQ2ZpZWxkQkxIVFMlMkNmaWVsZEFoaWRkZW4lMkNmaWVsZEZZWlNIJTJDZmllbGRKU1NKJTJDZmllbGRDWExCJTJDZmllbGRTUVNKJTJDZmllbGRDc2hyMyUyQ2ZpZWxkVFpTRkpLJTJDZmllbGRBU0ZaSE0lMkNmaWVsZENOJTJDZmllbGRGWVpTSFJRJTJDZmllbGRDWFNKRlJPTSUyQ2ZpZWxkRllaU0hSJTJDZmllbGRDc2hkYXRlMyUyQ2ZpZWxkWFNTRiUyQ2ZpZWxkQ3Noc2o1JTJDZmllbGRBanRkZCUyQ2ZpZWxkQXh5JTJDZmllbGRIU0JHJTJDZmllbGRDc2hkYXRlNCUyQ2ZpZWxkQWZkeSUyQ2ZpZWxkQ1hTWSUyQ2ZpZWxkQWRzJTJDZmllbGRDc2hyNCUyQ2ZpZWxkQ3NocjUlMkNmaWVsZEN5ajMlMkNmaWVsZEN5ajUlMkNmaWVsZEN5ajQlMkNmaWVsZEFzaGlzJmNzcmZUb2tlbj17NH0mbGFuZz16aAoKCiU3QiUyMl9WQVJfRVhFQ1VURV9JTkRFUF9PUkdBTklaRV9OYW1lJTIyJTNBJTIyJUU1JUJDJUEwJUU0JUI4JTg5JUU1JUFEJUE2JUU5JTk5JUEyJTIyJTJDJTIyX1ZBUl9BQ1RJT05fSU5ERVBfT1JHQU5JWkVTX0NvZGVzJTIyJTNBJTIyezZ9JTIyJTJDJTIyX1ZBUl9BQ1RJT05fUkVBTE5BTUUlMjIlM0ElMjIlRTUlQkMlQTAlRTQlQjglODklRTQlQjglODklMjIlMkMlMjJfVkFSX0FDVElPTl9PUkdBTklaRSUyMiUzQSUyMns2fSUyMiUyQyUyMl9WQVJfRVhFQ1VURV9PUkdBTklaRSUyMiUzQSUyMns2fSUyMiUyQyUyMl9WQVJfQUNUSU9OX0lOREVQX09SR0FOSVpFJTIyJTNBJTIyezZ9JTIyJTJDJTIyX1ZBUl9BQ1RJT05fSU5ERVBfT1JHQU5JWkVfTmFtZSUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNSVBRCVBNiVFOSU5OSVBMiUyMiUyQyUyMl9WQVJfQUNUSU9OX09SR0FOSVpFX05hbWUlMjIlM0ElMjIlRTUlQkMlQTAlRTQlQjglODklRTUlQUQlQTYlRTklOTklQTIlMjIlMkMlMjJfVkFSX0VYRUNVVEVfT1JHQU5JWkVTX05hbWVzJTIyJTNBJTIyJUU1JUJDJUEwJUU0JUI4JTg5JUU1JUFEJUE2JUU5JTk5JUEyJTIyJTJDJTIyX1ZBUl9PV05FUl9PUkdBTklaRVNfQ29kZXMlMjIlM0ElMjJ7Nn0lMjIlMkMlMjJfVkFSX0FERFIlMjIlM0ElMjIxMC4xMDAuMTE3LjIwJTIyJTJDJTIyX1ZBUl9MQVNUX0FDVElPTiUyMiUzQSUyMlN1Ym1pdCUyMiUyQyUyMl9WQVJfT1dORVJfT1JHQU5JWkVTX05hbWVzJTIyJTNBJTIyJUU1JUJDJUEwJUU0JUI4JTg5JUU1JUFEJUE2JUU5JTk5JUEyJTIyJTJDJTIyX1ZBUl9VUkwlMjIlM0ElMjJodHRwcyUzQSUyRiUyRmVoYWxsLm51YWEuZWR1LmNuJTJGaW5mb3BsdXMlMkZmb3JtJTJGezB9JTJGcmVuZGVyJTNGdGhlbWUlM0RudWFhX25ldyUyMiUyQyUyMl9WQVJfRVhFQ1VURV9PUkdBTklaRV9OYW1lJTIyJTNBJTIyJUU1JUJDJUEwJUU0JUI4JTg5JUU1JUFEJUE2JUU5JTk5JUEyJTIyJTJDJTIyX1ZBUl9SRUxFQVNFJTIyJTNBJTIydHJ1ZSUyMiUyQyUyMl9WQVJfVE9EQVklMjIlM0ElMjJ7NX0lMjIlMkMlMjJfVkFSX05PV19NT05USCUyMiUzQSUyMjklMjIlMkMlMjJfVkFSX0FDVElPTl9VU0VSQ09ERVMlMjIlM0ElMjIxNjIwMTAyMTklMjIlMkMlMjJfVkFSX0FDVElPTl9BQ0NPVU5UJTIyJTNBJTIyMTYyMDEwMjE5JTIyJTJDJTIyX1ZBUl9BQ1RJT05fSU5ERVBfT1JHQU5JWkVTX05hbWVzJTIyJTNBJTIyJUU1JUJDJUEwJUU0JUI4JTg5JUU1JUFEJUE2JUU5JTk5JUEyJTIyJTJDJTIyX1ZBUl9PV05FUl9BQ0NPVU5UJTIyJTNBJTIyMTYyMDEwMjE5JTIyJTJDJTIyX1ZBUl9BQ1RJT05fT1JHQU5JWkVTX05hbWVzJTIyJTNBJTIyJUU1JUJDJUEwJUU0JUI4JTg5JUU1JUFEJUE2JUU5JTk5JUEyJTIyJTJDJTIyX1ZBUl9TVEVQX0NPREUlMjIlM0ElMjJTUVIlMjIlMkMlMjJfVkFSX09XTkVSX1BIT05FJTIyJTNBJTIyMTIzNDU2Nzg5NDUlMjIlMkMlMjJfVkFSX09XTkVSX1VTRVJDT0RFUyUyMiUzQSUyMjE2MjAxMDIxOSUyMiUyQyUyMl9WQVJfRVhFQ1VURV9PUkdBTklaRVNfQ29kZXMlMjIlM0ElMjJ7Nn0lMjIlMkMlMjJfVkFSX05PV19EQVklMjIlM0ElMjIxJTIyJTJDJTIyX1ZBUl9PV05FUl9SRUFMTkFNRSUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNCVCOCU4OSUyMiUyQyUyMl9WQVJfRU5UUllfVEFHUyUyMiUzQSUyMjAxLSVFNyU5NiVBQiVFNiU4MyU4NSVFOSU5OCVCMiVFNiU4RSVBNyVFNiU5QyU4RCVFNSU4QSVBMSUyQyVFNyVBNyVCQiVFNSU4QSVBOCVFNyVBQiVBRiUyMiUyQyUyMl9WQVJfTk9XJTIyJTNBJTIyMTY2MjAzMzAwOCUyMiUyQyUyMl9WQVJfUEFSVElDSVBBTlRTJTIyJTNBJTIyJTJDMTYyMDEwMjE5JTJDJTIyJTJDJTIyX1ZBUl9VUkxfQXR0ciUyMiUzQSUyMiU3QiU1QyUyMnRoZW1lJTVDJTIyJTNBJTVDJTIybnVhYV9uZXclNUMlMjIlN0QlMjIlMkMlMjJfVkFSX0VOVFJZX05VTUJFUiUyMiUzQSUyMjEzMzU3Mzk3JTIyJTJDJTIyX1ZBUl9FWEVDVVRFX0lOREVQX09SR0FOSVpFU19OYW1lcyUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNSVBRCVBNiVFOSU5OSVBMiUyMiUyQyUyMl9WQVJfRU5UUllfTkFNRSUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNCVCOCU4OV8lRTclOTYlQUIlRTYlODMlODUlRTklOTglQjIlRTYlOEUlQTclRTYlOUMlOUYlRTUlQUQlQTYlRTclOTQlOUYlRTklOUIlQjYlRTYlOTglOUYlRTglQkYlOUIlRTUlODclQkElRTYlQTAlQTElRTclOTQlQjMlRTglQUYlQjclMjIlMkMlMjJfVkFSX1NURVBfTlVNQkVSJTIyJTNBJTIyezB9JTIyJTJDJTIyX1ZBUl9QT1NJVElPTlMlMjIlM0ElMjJ7Nn0lM0ExMSUzQTE2MjAxMDIxOSUyMiUyQyUyMl9WQVJfQUNUSU9OX1BIT05FJTIyJTNBJTIyMTIzNDU2Nzg5NDUlMjIlMkMlMjJfVkFSX0VYRUNVVEVfSU5ERVBfT1JHQU5JWkVTX0NvZGVzJTIyJTNBJTIyezZ9JTIyJTJDJTIyX1ZBUl9FWEVDVVRFX1BPU0lUSU9OUyUyMiUzQSUyMns2fSUzQTExJTNBMTYyMDEwMjE5JTIyJTJDJTIyX1ZBUl9BQ1RJT05fT1JHQU5JWkVTX0NvZGVzJTIyJTNBJTIyezZ9JTIyJTJDJTIyX1ZBUl9FWEVDVVRFX0lOREVQX09SR0FOSVpFJTIyJTNBJTIyezZ9JTIyJTJDJTIyX1ZBUl9OT1dfWUVBUiUyMiUzQSUyMjIwMjIlMjIlMkMlMjJncm91cFFXRERMaXN0JTIyJTNBJTVCMCU1RCUyQyUyMmZpZWxkSE1ERlolMjIlM0ElMjIyJTIyJTJDJTIyZmllbGRYU1NGJTIyJTNBJTIyJUU2JTlDJUFDJUU3JUE3JTkxJUU3JTk0JTlGJTIyJTJDJTIyZmllbGRTUVNKJTIyJTNBMTY2MjAzMzAwOCUyQyUyMmZpZWxkQXhtJTIyJTNBJTIyMTYyMDEwMjE5JTIyJTJDJTIyZmllbGRBeG1fTmFtZSUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNCVCOCU4OSUyMiUyQyUyMmZpZWxkQXh5JTIyJTNBJTIyezZ9JTIyJTJDJTIyZmllbGRBeHlfTmFtZSUyMiUzQSUyMiVFNSVCQyVBMCVFNCVCOCU4OSVFNSVBRCVBNiVFOSU5OSVBMiUyMiUyQyUyMmZpZWxkQXhoJTIyJTNBJTIyMTYyMDEwMjE5JTIyJTJDJTIyZmllbGRBbHhkaCUyMiUzQSUyMjEyMzQ1Njc4OTQ1JTIyJTJDJTIyZmllbGRBZmR5JTIyJTNBJTIyezF9JTIyJTJDJTIyZmllbGRBZmR5X05hbWUlMjIlM0ElMjIlRTUlQkMlQTAlRTQlQjglODklRTQlQjglODklMjIlMkMlMjJmaWVsZERTJTIyJTNBJTIyJTIyJTJDJTIyZmllbGREU19OYW1lJTIyJTNBJTIyJTIyJTJDJTIyZmllbGRBU0ZaSE0lMjIlM0ElMjIxMjM0NTY3ODk0NTYxMjM0NTYlMjIlMkMlMjJmaWVsZEFTWlhRJTIyJTNBJTIyMiUyMiUyQyUyMmZpZWxkQVNaWFFfTmFtZSUyMiUzQSUyMiVFNSVCMCU4NiVFNSU4NiU5QiVFOCVCNyVBRiVFNiVBMCVBMSVFNSU4QyVCQSUyMiUyQyUyMmZpZWxkWFNMWCUyMiUzQSUyMiVFNCVCRCU4RiVFNiVBMCVBMSUyMiUyQyUyMmZpZWxkWFNMWF9OYW1lJTIyJTNBJTIyJUU0JUJEJThGJUU2JUEwJUExJTIyJTJDJTIyZmllbGRTRllHTFMlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZFRaU0ZKSyUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkU0tNJTIyJTNBJTIyJTdCJTVDJTIyaWQlNUMlMjIlM0ElNUMlMjIxZmE5ODRlNy04YTQyLTQwOTktOTAzYy0xMDFmNjVkMzI5ZjQlNUMlMjIlMkMlNUMlMjJuYW1lJTVDJTIyJTNBJTVDJTIyMS5wbmclNUMlMjIlMkMlNUMlMjJzaXplJTVDJTIyJTNBMSUyQyU1QyUyMnVyaSU1QyUyMiUzQSU1QyUyMmh0dHBzJTNBJTJGJTJGZWhhbGwubnVhYS5lZHUuY24lMkZmaWxlJTJGMWZhOTg0ZTctOGE0Mi00MDk5LTkwM2MtMTAxZjY1ZDMyOWY0JTVDJTIyJTJDJTVDJTIybWltZSU1QyUyMiUzQSU1QyUyMmltYWdlJTJGcG5nJTVDJTIyJTdEJTIyJTJDJTIyZmllbGRYQ00lMjIlM0ElMjIlN0IlNUMlMjJpZCU1QyUyMiUzQSU1QyUyMmI1OTBmMWRmLTA1MGItNDMyYi05OWVjLThkNjYzNTY2MDdkZiU1QyUyMiUyQyU1QyUyMm5hbWUlNUMlMjIlM0ElNUMlMjIxLnBuZyU1QyUyMiUyQyU1QyUyMnNpemUlNUMlMjIlM0ExJTJDJTVDJTIydXJpJTVDJTIyJTNBJTVDJTIyaHR0cHMlM0ElMkYlMkZlaGFsbC5udWFhLmVkdS5jbiUyRmZpbGUlMkZiNTkwZjFkZi0wNTBiLTQzMmItOTllYy04ZDY2MzU2NjA3ZGYlNUMlMjIlMkMlNUMlMjJtaW1lJTVDJTIyJTNBJTVDJTIyaW1hZ2UlMkZwbmclNUMlMjIlN0QlMjIlMkMlMjJmaWVsZEhTQkclMjIlM0ElMjIlN0IlNUMlMjJpZCU1QyUyMiUzQSU1QyUyMjI2ODQ2MDUyLWNiNTktNGNhZC1iMzlhLThjYjA0ZjlhNTcyZCU1QyUyMiUyQyU1QyUyMm5hbWUlNUMlMjIlM0ElNUMlMjIxLnBuZyU1QyUyMiUyQyU1QyUyMnNpemUlNUMlMjIlM0ExJTJDJTVDJTIydXJpJTVDJTIyJTNBJTVDJTIyaHR0cHMlM0ElMkYlMkZlaGFsbC5udWFhLmVkdS5jbiUyRmZpbGUlMkYyNjg0NjA1Mi1jYjU5LTRjYWQtYjM5YS04Y2IwNGY5YTU3MmQlNUMlMjIlMkMlNUMlMjJtaW1lJTVDJTIyJTNBJTVDJTIyaW1hZ2UlMkZwbmclNUMlMjIlN0QlMjIlMkMlMjJmaWVsZEJMSFRTJTIyJTNBJTIyJTIyJTJDJTIyZmllbGRDWFJRJTIyJTNBezV9JTJDJTIyZmllbGRKU1NKJTIyJTNBezV9JTJDJTIyZmllbGRDWFNKRlJPTSUyMiUzQTAlMkMlMjJmaWVsZENYU0pUTyUyMiUzQTMwMCUyQyUyMmZpZWxkQ1hTWSUyMiUzQSUyMi4uLiUyMiUyQyUyMmZpZWxkQ1hMQiUyMiUzQSUyMjElMjIlMkMlMjJmaWVsZEFjeHhjJTIyJTNBJTIyMiUyMiUyQyUyMmZpZWxkQWRzJTIyJTNBJTIyMSUyMiUyQyUyMmZpZWxkQXNoZW5ncyUyMiUzQSU1QiUyMiUyMiU1RCUyQyUyMmZpZWxkQXNoZW5nc19OYW1lJTIyJTNBJTVCJTIyJTIyJTVEJTJDJTIyZmllbGRBc2hpcyUyMiUzQSU1QiUyMiUyMiU1RCUyQyUyMmZpZWxkQXNoaXNfTmFtZSUyMiUzQSU1QiUyMiUyMiU1RCUyQyUyMmZpZWxkQXNoaXNfQXR0ciUyMiUzQSU1QiUyMiU3QiU1QyUyMl9wYXJlbnQlNUMlMjIlM0ElNUMlMjIlNUMlMjIlN0QlMjIlNUQlMkMlMjJmaWVsZEFqdGRkJTIyJTNBJTVCJTIyJTIyJTVEJTJDJTIyZmllbGRDTiUyMiUzQXRydWUlMkMlMjJmaWVsZEFoaWRkZW4lMjIlM0ElMjIlMjIlMkMlMjJmaWVsZEN5ajMlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENzaHIzJTIyJTNBJTIyJTIyJTJDJTIyZmllbGRDc2hyM19OYW1lJTIyJTNBJTIyJTIyJTJDJTIyZmllbGRDc2hkYXRlMyUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkRllaU0glMjIlM0ElMjIlMjIlMkMlMjJmaWVsZEZZWlNIUiUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkRllaU0hSX05hbWUlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZEZZWlNIUlElMjIlM0ElMjIlMjIlMkMlMjJmaWVsZEN5ajQlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENzaHI0JTIyJTNBJTIyJTIyJTJDJTIyZmllbGRDc2hyNF9OYW1lJTIyJTNBJTIyJTIyJTJDJTIyZmllbGRDc2hkYXRlNCUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkQ3lqNSUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkQ3NocjUlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENzaHI1X05hbWUlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENzaHNqNSUyMiUzQSUyMiUyMiUyQyUyMmZpZWxkVE9LRU4lMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENYUlFTVFIlMjIlM0ElMjIlMjIlMkMlMjJmaWVsZENYUlFGcm9tJTIyJTNBezV9JTJDJTIyZmllbGRGWlpEJTIyJTNBJTIyJTIyJTdEJnJlbWFyaz0mcmFuZD0zNjUuNzAyNzA5MDU5ODM1OTcmbmV4dFVzZXJzPSU3QiUyMjIlMkMlMjIlM0ElMjI3Yzk0YzBjMy1jOTVlLTExZTktOTEyNy0wMDUwNTY4YTI4MWYlMjIlN0Qmc3RlcElkPXswfSZ0aW1lc3RhbXA9ezJ9JmJvdW5kRmllbGRzPWZpZWxkQ1hTSlRPJTJDZmllbGRBU1pYUSUyQ2ZpZWxkQ1hSUSUyQ2ZpZWxkQXNoZW5ncyUyQ2ZpZWxkQWN4eGMlMkNmaWVsZEF4aCUyQ2ZpZWxkRlpaRCUyQ2ZpZWxkQ1hSUVNUUiUyQ2ZpZWxkU0tNJTJDZmllbGRBeG0lMkNmaWVsZEFseGRoJTJDZmllbGRDWFJRRnJvbSUyQ2ZpZWxkRFMlMkNmaWVsZFhDTSUyQ2ZpZWxkVE9LRU4lMkNmaWVsZFhTTFglMkNmaWVsZFNGWUdMUyUyQ2ZpZWxkSE1ERlolMkNmaWVsZEJMSFRTJTJDZmllbGRBaGlkZGVuJTJDZmllbGRGWVpTSCUyQ2ZpZWxkSlNTSiUyQ2ZpZWxkQ1hMQiUyQ2ZpZWxkU1FTSiUyQ2ZpZWxkQ3NocjMlMkNmaWVsZFRaU0ZKSyUyQ2ZpZWxkQVNGWkhNJTJDZmllbGRDTiUyQ2ZpZWxkRllaU0hSUSUyQ2ZpZWxkQ1hTSkZST00lMkNmaWVsZEZZWlNIUiUyQ2ZpZWxkQ3NoZGF0ZTMlMkNmaWVsZFhTU0YlMkNmaWVsZENzaHNqNSUyQ2ZpZWxkQWp0ZGQlMkNmaWVsZEF4eSUyQ2ZpZWxkSFNCRyUyQ2ZpZWxkQ3NoZGF0ZTQlMkNmaWVsZEFmZHklMkNmaWVsZENYU1klMkNmaWVsZEFkcyUyQ2ZpZWxkQ3NocjQlMkNmaWVsZENzaHI1JTJDZmllbGRDeWozJTJDZmllbGRDeWo1JTJDZmllbGRDeWo0JTJDZmllbGRBc2hpcyZjc3JmVG9rZW49ezR9Jmxhbmc9emg)

# 天气

[零成本打造 Telegram 机器人指北](https://changchen.me/blog/20210221/buld-telegram-bot-from-scratch/)

# References

[GitHub - python-telegram-bot/python-telegram-bot: We have made you a wrapper you can&#39;t refuse](https://github.com/python-telegram-bot/python-telegram-bot)

## 官方API文档

[Telegram Bot API](https://core.telegram.org/bots/api)

中文

[Telegram Bot 使用文档](https://www.cnblogs.com/kainhuck/p/13576012.html)

## 机器人头像

[Notion 风格头像制作](https://notion-avatar.vercel.app/zh)

## 消息格式

[python-telegram-bot/errorhandlerbot.py at master · python-telegram-bot/python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/errorhandlerbot.py)

## Notion API 封装

[notion应用笔记](https://www.zhihu.com/column/c_1389160991083692032)

[notion API命令-个性化再封装](https://zhuanlan.zhihu.com/p/395219868)

[notion应用笔记](https://www.zhihu.com/column/c_1389160991083692032)

[](https://blog.csdn.net/xinhuoip/article/details/117036010)

## 官方实例

[python-telegram-bot/echobot.py at master · python-telegram-bot/python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py)
