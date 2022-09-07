# 判断参数是否为三个
def check_Number_of_parameters(func):
    def wrapper(*args, **kwargs):
        if (len(args[1].args) != 3):
            message = (
                f"格式错误哦\~，需要三个参数，注意学号 密码 出校日期之间的空格\n\n"
                f"请输入 `/leave 学号 教务处密码 出校日期`\n\n"
                f"例如学号为 1234，密码是 123，出校日期 `2022\-9\-6`\n\n"
                f"则输入 `/leave 1234 123 2022\-9\-6`\n\n"
                f"日期务必用短横线隔开，👆点击上方命令复制格式\n\n"
            )
            args[1].bot.send_message(chat_id=args[0].effective_chat.id, text=message, parse_mode='MarkdownV2')
            return
        return func(*args, **kwargs)
    return wrapper

# 判断是否是授权用户
def check_Authorization(func):
    def wrapper(*args, **kwargs):
        from leave.config import raw
        if (args[1].args[0] not in raw):
            message = (
                f"本功能需要定制，请联系 @yym68686\n\n"
                f"后续就可以直接使用一条命令自动申请出校啦\~\n\n"
            )
            args[1].bot.send_message(chat_id=args[0].effective_chat.id, text=message, parse_mode='MarkdownV2')
            return
        return func(*args, **kwargs)
    return wrapper

# 判断日期格式是否正确
def check_Date_format(func):
    def wrapper(*args, **kwargs):
        import re
        regex = r"((((19|20)\d{2})-(0?(1|[3-9])|1[012])-(0?[1-9]|[12]\d|30))|(((19|20)\d{2})-(0?[13578]|1[02])-31)|(((19|20)\d{2})-0?2-(0?[1-9]|1\d|2[0-8]))|((((19|20)([13579][26]|[2468][048]|0[48]))|(2000))-0?2-29))$"
        leaveTime = re.findall(regex, args[1].args[2])
        if (len(leaveTime) == 0):
            message = (
                f"日期格式错误！\n\n"
                f"日期务必用短横线隔开，👇点击下方命令复制格式\n\n"
                f"`/leave 1234 123 2022\-9\-6`\n\n"
            )
            args[1].bot.send_message(chat_id=args[0].effective_chat.id, text=message, parse_mode='MarkdownV2')
            return
        return func(*args, **kwargs)
    return wrapper

# 判断日期是否大于等于当前日期
def check_Date_range(func):
    def wrapper(*args, **kwargs):
        import datetime
        todaydate = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d')
        inputdate = datetime.datetime.strptime(args[1].args[2], '%Y-%m-%d')
        if inputdate < todaydate:
            message = (
                f"申请日期不得小于当前日期！\n\n"
            )
            args[1].bot.send_message(chat_id=args[0].effective_chat.id, text=message, parse_mode='MarkdownV2')
            return
        return func(*args, **kwargs)
    return wrapper