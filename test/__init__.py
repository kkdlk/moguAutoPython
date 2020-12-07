import datetime

# 当前时间距离给定时间相差多少周
def week_num(start_time):
    week_start = datetime.strptime(start_time, '%Y-%m-%d')
    week_end = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
    return int(datetime.strftime(week_end, "%W")) - int(datetime.strftime(week_start, "%W"))+1


# print(week_num('2020-11-23'))

def getNum ():
    weekDay = datetime.now().weekday()
    dayOfWeek = datetime.now().isoweekday()  ###返回数字1-7代表周一到周日
    print(weekDay)

from datetime import datetime
print(datetime.now().year)
print(datetime.now().month)


'''
获取当前时间的周一周末的具体时间
'''
def get_current_week():
    import datetime
    monday, sunday = datetime.date.today(), datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day

    return datetime.datetime.strftime(monday, "%Y-%m-%d") + ' 00:00:00', datetime.datetime.strftime(sunday, "%Y-%m-%d")+ ' 23:59:59'











