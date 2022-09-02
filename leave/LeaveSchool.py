import re
import sys
import time
import asyncio
import leave.HackRequests
from datetime import date
from pyppeteer import launch
from leave.config import GetStepIdraw, raw

# 获取 cookies
async def getJSESSIONID(username, password):
    # browser = await launch(headless=False, args=['--disable-infobars'])
    browser = await launch()
    page = await browser.newPage()
    # 绕过 WebDriver 的检测，在每次加载网页的时候执行语句，执行将 WebDriver 隐藏的命令
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
    # 设置页面视图大小
    await page.setViewport(viewport={'width': 1280, 'height': 800})
    # 是否启用JS，enabled设为False，则无渲染效果
    await page.setJavaScriptEnabled(enabled=True)
    res = await page.goto('https://ehall.nuaa.edu.cn/infoplus/form/YQFKXSFXLSCX_CS/start?theme=nuaa_new')
    await page.waitForSelector("#login_submit")
    await page.type('#username', username)
    await page.type('#password', password)
    await page.click('#login_submit')
    await page.waitForSelector("#preview_start_button")
    # 打印页面cookies
    cookie = await page.cookies()
    # print(cookie[1]["value"])
    # 关闭浏览器
    await browser.close()
    return cookie[1]["value"]

def POSTraw(username, password, leavetime):
    # 变量配置
    stepId = ""
    csrfToken = "tkx6BTNaH8Fy4hNKawyjhDMVDBdvrD2i"
    today = str(date.today()).split("-")
    # 今天的月份
    todaymonth = today[1]
    # 今天的日份
    todayday = today[2]
    # 当前时间戳
    timestamp = int(time.time())
    # 获取 cookies
    jsessionID = asyncio.get_event_loop().run_until_complete(getJSESSIONID(username, password, interruptable=False))
    # 不可以用 jsessionID = asyncio.get_event_loop().run_until_complete(getJSESSIONID(username, password))
    # 在主线程中，调用get_event_loop总能返回属于主线程的event loop对象，如果是处于非主线程中，还需要调用set_event_loop方法指定一个event loop对象，这样get_event_loop才会获取到被标记的event loop对象
    # new_loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(new_loop)
    # loop = asyncio.get_event_loop()
    # # task = asyncio.ensure_future()
    # jsessionID = loop.run_until_complete(getJSESSIONID(username, password))
    # loop.close()
    print("jsessionID", jsessionID)
    # 0515000 航天学院
    # 0518000 长空学院
    Studept = "0501000"

    # 获取新的离校申请 ID
    hack = HackRequests.hackRequests()
    for _ in range(3):
        hh = hack.httpraw(GetStepIdraw.format(todaymonth, todayday, csrfToken, timestamp, jsessionID, Studept),ssl=type)
        test_str = hh.text()
        if ("SAFETY_PROTECTION_CSRF" in test_str):
            csrfToken = re.findall(r"\[\"(.*?)\"]", test_str)[0]
            print("csrfToken", csrfToken)
        elif ("SYSTEM_BUSY" in test_str):
            print("system busy...")
            exit(0)
        elif ("USER_LOGIN_REQUIRED" in test_str):
            print("need login, JSESSIONID expired...")
            exit(0)
        else:
            print(test_str)
            stepId = re.findall(r"form/(.*?)/render", test_str)[0]
            if not stepId:
                print("get step id error!")
                exit(0)
            print("stepId", stepId)
            break

    # 使用 POST 请求体发送离校申请

    # 获取离校日期时间戳
    postraw = raw[username]["raw"]
    fieldAfdy = raw[username]["fieldAfdy"]
    leaveSchool_timestamp = int(time.mktime(time.strptime(leavetime + ' 00:00:00', '%Y-%m-%d %H:%M:%S')))
    hh = hack.httpraw(postraw.format(stepId, fieldAfdy, timestamp, jsessionID, csrfToken, leaveSchool_timestamp, Studept), ssl=type)
    test_str = hh.text()
    print(test_str)
    if ("SUCCEED" in test_str):
        return "已成功申请！出校愉快~"
    else:
        return "嘤嘤嘤~，出错啦！"

if __name__ == '__main__':
    POSTraw(sys.argv[1], sys.argv[2], sys.argv[3])