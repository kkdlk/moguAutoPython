import json
import requests
import datetime



'''
读取一个本地Json文件
'''
def readJsonFile(filePath):
    print("开始读取本地json文件，文件地址：" + filePath)
    try:
        with open(file=filePath, mode="r", encoding="utf-8-sig") as  load_f:
            load_result = json.load(load_f)
            # print(load_result)
            if (load_result):
                return load_result
            else:
                return False
    except:
        print("读取本地Json文件错误，请检查地址!" + filePath)
        pass
'''
Post请求Url
'''
def PostUrl(url, headers, data):
    requests.packages.urllib3.disable_warnings()
    resp = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    return resp.json()
def postNoHeader(url, data):
    resp = requests.post(url,data=data, stream=True, verify=False, allow_redirects=False)
    return resp.json()
'''
Get请求
'''
def GetUrl(url, headers, data):
    requests.packages.urllib3.disable_warnings()
    resp = requests.get(url, headers=headers, data=json.dumps(data), verify=False)
    return resp.json()

'''
判断设置的时间是否比现在时间大（是否可用）过期返回false 可用返回True 
传来过期时间
'''
# 签到服务是否结束
def isSign(expirationTime):
    nowHour = datetime.datetime.now().date() #当前时间
    print("当前时间是:"+str(nowHour))
    print("过期时间是:"+expirationTime)
    # d_time = datetime.datetime.strptime('2020-4-12 23:34:34', '%Y-%m-%d %H:%M:%S')
    d_time = datetime.datetime.strptime(str(expirationTime), '%Y-%m-%d').date() #过期时间 '2020-12-7'
    print('未过期' if d_time>=nowHour else '已过期')
    # print(d_time>=nowHour)
    return d_time>=nowHour #过期时间大于当前时间

'''
发送方糖消息
'''
def sendMsg(sckey,readMsg):
    if (sckey):
        url = 'http://sc.ftqq.com/'+sckey+'.send'
        resp = postNoHeader(url,readMsg)
        if (resp['errno'] == 0):
            print("消息发送成功")
        else:
            print("------------消息发送失败失败标题"+readMsg['text'])
    else:
        print("------------未设置消息key值，发送失败------------")
'''
 当前时间距离给定时间相差多少周 start_time 开始时间
'''
def week_num(start_time):
    from datetime import datetime
    week_start = datetime.strptime(start_time, '%Y-%m-%d')
    week_end = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
    return int(datetime.strftime(week_end, "%W")) - int(datetime.strftime(week_start, "%W"))+1


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


