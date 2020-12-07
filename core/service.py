from utils.UtilsClass import readJsonFile
from utils.UtilsClass import PostUrl
from utils.UtilsClass import isSign
from core.GetToken import getTokenGetToken
from core.signCoreAction import sign
from core.signCoreAction import daySign
from core.signCoreAction import weekSign
from core.signCoreAction import monthSign
import time

'''
通过Token 获取planId
'''

def GetPlanId(token):
    planUrl = readJsonFile("../conf/urlMain.json")['planUrl']
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
        'roleKey': 'student',
        'Authorization': token
    }
    data = {"paramsType": "student"}
    resp = PostUrl(planUrl, headers, data)
    print(resp['msg'])
    if (resp['code'] == 200):
        print("获取到PlanId" + resp['data'][0]['planId'])
        return resp['data'][0]['planId']
    elif (resp['code'] == 401):
        print("Token已过期，不可用")
        return False
    else:
        print("程序异常" + resp)
        return


'''
批量获取planId
'''
def getBatchAccountToken():
    accountJsons =  readJsonFile("../conf/main.json")
    for accountInfo in accountJsons['loginData']:#循环遍历json数组
        if (isSign(accountInfo['endSign'])): #判断服务是否过期
            tokenStr = getTokenGetToken(accountInfo['phone'],accountInfo['password'],accountInfo['token'])#校验或登录获取token
            if (tokenStr=='444'):
                print(accountInfo['kkdaj'] + "错误,程序停止！")
                return;
            ##到这里就说明得到了json
            ## 这个时候就修改json文件中的token --------未完成-----------
            planId = GetPlanId(tokenStr)
            if (planId):
                print('1、'+accountInfo['kkdaj']+'手机号'+accountInfo['phone']+"开始执行每日签到")
                sign(tokenStr,planId,accountInfo) #每日签到
                time.sleep(2)
                print('2、' + accountInfo['kkdaj'] + '手机号' + accountInfo['phone'] + "开始执行每日日报")
                daySign(tokenStr,planId,accountInfo) #每日日报
                time.sleep(2)
                print('3、' + accountInfo['kkdaj'] + '手机号' + accountInfo['phone'] + "开始执行每周周报")
                weekSign(tokenStr,planId,accountInfo) #每周周报
                time.sleep(2)
                print('4、' + accountInfo['kkdaj'] + '手机号' + accountInfo['phone'] + "开始执行每月月报")
                monthSign(tokenStr,planId,accountInfo) #每月月报
                print("-!---------------程序执行完毕，请查看日志核实是否成功！------------!-------")
            else:
                return False;
        else:
            print(accountInfo['kkdaj']+"的服务已结束，请及时续费")
            return False;



getBatchAccountToken()