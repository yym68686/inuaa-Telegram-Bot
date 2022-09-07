import datetime

todaydate = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d')
inputdate = datetime.datetime.strptime("2022-9-07", '%Y-%m-%d')
if inputdate >= todaydate:
    print(True)
else:
    print(False)