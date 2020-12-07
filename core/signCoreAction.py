'''
作者：KKDAJ
功能：签到核心代码
DateTime: 2020年12月5日00:19:56
'''
from datetime import datetime
from utils.UtilsClass import PostUrl
from utils.UtilsClass import readJsonFile
from utils.UtilsClass import sendMsg
from utils.UtilsClass import get_current_week
from utils.UtilsClass import week_num
from core.signContxt import randDayTxt
from core.signContxt import randWeekTxt

'signOnDate上班时间signOutDate下班时间'
def signType(signOnDate, signOutDate):
    nowHour = datetime.now().hour
    if (int(nowHour) == int(signOnDate)):
        type = "START"
        return type
    elif (int(nowHour) == int(signOutDate)):
        type = "END"
        return type
    else:
        print("----------不在上班或下班时间，错误！！-----------")
        return False;


'''每日签到方法'''
def sign(token, planId, accountInfo):
    signOnDate = accountInfo['signOnDate']  # 上班的打卡时间
    signOutDate = accountInfo['signOutDate']  # 下班的打卡时间
    type = signType(signOnDate, signOutDate)  # 上班还是下班打卡
    province = accountInfo['province']  # 市
    city = accountInfo['city']  # 区
    address = accountInfo['address']  # 地址
    longitude = accountInfo['longitude']  # 经度
    latitude = accountInfo['latitude']  # 纬度
    sckey = accountInfo['sckey']  # Server秘钥
    nowDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if type:
        staticType = '上班' if type == 'START' else '下班' + '签到成功'
        readMsg = {
            'text': nowDate + accountInfo['kkdaj'] + staticType,
            'desp': '请注意自身安全，蘑菇丁并不只是麻烦，如遇到危险请及时拨打【110】\n'
                    + '1、陷入传销多半会被限人身自由，并且传销人zhi员众多，要用智慧逃脱，强行逃走很可能会被殴打。\n'
                    + '2、如果遇到24小时有人“跟踪陪伴”软监视自己，可以借机向路人求助，或者见到当地执法单位，交警、巡警、派出所、工商局、检查院、立即躲进寻求帮助或者在钱币或者纸条上写上求助原因扔向窗外。\n'
                    + '3、中国目前传销组织多数都是以“人性化”操作，不强迫威胁参与，可以随时退出，要充份开动脑筋与传销人员周旋尽快离开，不要轻信他们的谎言，导致被“洗脑”。\n'
                    + '4、冷静面对，不要急燥害怕，控制自己的情绪，利用技巧与传销人员周旋。降低传销人员对本人的防惫心，找理由逃离传销组织。\n'
                    + '例如：假装相信传销组织谎言，身上没钱参与，回家取钱为由离开。'
        }
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
            'Authorization': token
        }
        dataForm = {
            'device': "android",
            'planId': planId,
            'country': "中国",
            'state': "NORMAL",
            'attendanceType': "",
            'address': address,
            'type': type,
            'longitude': longitude,
            'city': city,
            'province': province,
            'latitude': latitude
        }
        resp = PostUrl(readJsonFile("../conf/urlMain.json")['signUrl'], headers, dataForm)
        if (resp['code'] == 200):
            sendMsg(sckey, readMsg);
            print(accountInfo['kkdaj'] + type + "=========签到成功========" + staticType)
            return  staticType
        else:
            readMsg['text'] = nowDate + staticType + '---------签到失败-------'
            sendMsg(sckey, readMsg);
            print(accountInfo['kkdaj'] + type + "---------签到失败-------")
            return False
    else:
        print("------不在用户设置的签到和签退时间内，拒绝签到---------")
        return False


'''日报汇报'''
def daySign(token, planId, accountInfo):
    leableati = accountInfo['leableati']  # 专业
    daySign = accountInfo['daySign']  # 日报时间
    nowHour = datetime.now().hour  # 当前时间几点
    sckey = accountInfo['sckey']  # Server秘钥
    nowDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if int(daySign) == nowHour: #获取日报汇报时间（几点）比较是否发送日报
        content = randDayTxt(leableati, 3)  # 生成内容
        title = isWeekVacation()  # 生成标题
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
            'Authorization': token
        }
        dataForm = {
            'attachmentList': [],
            'attachments': "",
            'content': content,
            'planId': planId,
            'reportType': "day",
            'title': title
        }
        readMsg = {
            'text': nowDate + accountInfo['kkdaj'] +'日报成功',
            'desp': '请注意自身安全，蘑菇丁并不只是麻烦，如遇到危险请及时拨打【110】\n'
                    + '1、陷入传销多半会被限人身自由，并且传销人zhi员众多，要用智慧逃脱，强行逃走很可能会被殴打。\n'
                    + '2、如果遇到24小时有人“跟踪陪伴”软监视自己，可以借机向路人求助，或者见到当地执法单位，交警、巡警、派出所、工商局、检查院、立即躲进寻求帮助或者在钱币或者纸条上写上求助原因扔向窗外。\n'
                    + '3、中国目前传销组织多数都是以“人性化”操作，不强迫威胁参与，可以随时退出，要充份开动脑筋与传销人员周旋尽快离开，不要轻信他们的谎言，导致被“洗脑”。\n'
                    + '4、冷静面对，不要急燥害怕，控制自己的情绪，利用技巧与传销人员周旋。降低传销人员对本人的防惫心，找理由逃离传销组织。\n'
                    + '例如：假装相信传销组织谎言，身上没钱参与，回家取钱为由离开。'
        }
        resp = PostUrl(readJsonFile("../conf/urlMain.json")['reportUrl'], headers, dataForm)
        if (resp['code'] == 200):
            print(accountInfo['kkdaj'] + '=======日报成功=======')
            sendMsg(sckey, readMsg);
            return '日报成功'

        else:
            readMsg['text'] = nowDate +'---------日报失败--------'
            sendMsg(sckey, readMsg);
            print(accountInfo['kkdaj'] + '---------日报失败-------')
            return False
    else:
        print("不在每日日报时间！不进行日报打卡")
        return False

# 根据当前周生成标题
def isWeekVacation():
    weekDay = datetime.now().weekday()
    if weekDay == 5 or weekDay == 6 :
        return "休假"
    else:
        return "上班"
'''
周报汇报
'''
def weekSign(token, planId, accountInfo):
    startWeekTime = accountInfo['startWeekTime']  # 周报开始时间计算当前周是第几周
    weekDate = accountInfo['weekDate'] #每周周报时间（周几开始执行签到方法，返回数字1-7代表周一到周日）
    nowHour = datetime.now().hour  # 当前时间几点
    sckey = accountInfo['sckey']  # Server秘钥
    nowDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #当前具体时间
    weekNum = week_num(startWeekTime) #当前周距离设置的开始周 相差多少周
    if  datetime.now().isoweekday()==int(weekDate) and nowHour==8: ### datetime.now().isoweekday() 返回数字1-7代表周一到周日
        #生成周报内容
        weekContent = randWeekTxt(weekNum)
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
            'Authorization': token
        }
        dataForm = {
           'attachmentList': [],
           'attachments': "",
            'content': weekContent, #// 周报内容
            'planId': planId,
            'reportType': "week",
            'title': "第" + str(weekNum) + "周，周报", #// 周报标题
            'weeks': "第" + str(weekNum) + "周", #// 第x周从startTimeDate开始
            'startTime': get_current_week()[0], #// 当前周开始时间
            'endTime': get_current_week()[1]#// 当前周结束时间
        }
        readMsg = {
            'text': nowDate + accountInfo['kkdaj'] + '周报成功',
            'desp': '请注意自身安全，蘑菇丁并不只是麻烦，如遇到危险请及时拨打【110】\n'
                    + '1、陷入传销多半会被限人身自由，并且传销人zhi员众多，要用智慧逃脱，强行逃走很可能会被殴打。\n'
                    + '2、如果遇到24小时有人“跟踪陪伴”软监视自己，可以借机向路人求助，或者见到当地执法单位，交警、巡警、派出所、工商局、检查院、立即躲进寻求帮助或者在钱币或者纸条上写上求助原因扔向窗外。\n'
                    + '3、中国目前传销组织多数都是以“人性化”操作，不强迫威胁参与，可以随时退出，要充份开动脑筋与传销人员周旋尽快离开，不要轻信他们的谎言，导致被“洗脑”。\n'
                    + '4、冷静面对，不要急燥害怕，控制自己的情绪，利用技巧与传销人员周旋。降低传销人员对本人的防惫心，找理由逃离传销组织。\n'
                    + '例如：假装相信传销组织谎言，身上没钱参与，回家取钱为由离开。'
        }
        resp = PostUrl(readJsonFile("../conf/urlMain.json")['reportUrl'], headers, dataForm)
        if (resp['code'] == 200):
            print(accountInfo['kkdaj'] + '======周报成功======')
            sendMsg(sckey, readMsg);
            return '周报成功'
        else:
            readMsg['text'] = nowDate +'-------周报失败---------'
            sendMsg(sckey, readMsg);
            print(accountInfo['kkdaj'] + '--------周报失败-------')
            return False
    else:
        print(accountInfo['kkdaj']+"的周报不在设置的时间内,设置时间为每周周"+weekDate+'早上8点')
        return False
'''
月报汇报
'''
def monthSign(token, planId, accountInfo):
    leableati = accountInfo['leableati']  # 专业
    monthDate = accountInfo['monthDate']  # 月报在每月几号开始
    nowHour = datetime.now().hour  # 当前时间几点
    nowDay = datetime.now().day  # 当前时间是本月的几号
    sckey = accountInfo['sckey']  # Server秘钥
    nowDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if nowDay == int(monthDate) and nowHour == 8:
        monthTitle = (datetime.now().year) + "年" + (datetime.now().month) + "月" + ",月报。" #生成标题
        monthContent = randDayTxt(leableati,7)  # 生成内容
        dataForm = {
               'attachmentList': [],
               'attachments': "",
               'content': monthContent, #// 月报内容
                'planId': planId,
                'reportType': "month",
                'title': monthTitle #// 月报标题上班或休假每周有2天休假的时间
        }
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
            'Authorization': token
        }
        readMsg = {
            'text': nowDate + accountInfo['kkdaj'] + '月报成功',
            'desp': '请注意自身安全，蘑菇丁并不只是麻烦，如遇到危险请及时拨打【110】\n'
                    + '1、陷入传销多半会被限人身自由，并且传销人zhi员众多，要用智慧逃脱，强行逃走很可能会被殴打。\n'
                    + '2、如果遇到24小时有人“跟踪陪伴”软监视自己，可以借机向路人求助，或者见到当地执法单位，交警、巡警、派出所、工商局、检查院、立即躲进寻求帮助或者在钱币或者纸条上写上求助原因扔向窗外。\n'
                    + '3、中国目前传销组织多数都是以“人性化”操作，不强迫威胁参与，可以随时退出，要充份开动脑筋与传销人员周旋尽快离开，不要轻信他们的谎言，导致被“洗脑”。\n'
                    + '4、冷静面对，不要急燥害怕，控制自己的情绪，利用技巧与传销人员周旋。降低传销人员对本人的防惫心，找理由逃离传销组织。\n'
                    + '例如：假装相信传销组织谎言，身上没钱参与，回家取钱为由离开。'
        }
        resp = PostUrl(readJsonFile("../conf/urlMain.json")['reportUrl'], headers, dataForm)
        if (resp['code'] == 200):
            print(accountInfo['kkdaj'] + '======月报成功======')
            sendMsg(sckey, readMsg);
            return '月报成功'
        else:
            readMsg['text'] = nowDate + '-------月报失败---------'
            sendMsg(sckey, readMsg);
            print(accountInfo['kkdaj'] + '--------月报失败-------')
            return False
    else:
        print(accountInfo['kkdaj']+"的月报不在设置的时间内,设置时间为每月"+monthDate+'号，早上8点')
        return False