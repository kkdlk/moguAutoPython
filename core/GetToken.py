from utils.UtilsClass import readJsonFile
from utils.UtilsClass import PostUrl




headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36'
    }


'''
作者：KKDAJ
功能：整合校验和登录功能
DateTime: 2020年12月5日00:19:56
'''


def getTokenGetToken(phone, password, token):
    ## token未设置，跳过校验token
    if (token != ""):
        if (istoken(token)):
            return token
        else:
            nowToken = login(phone, password)
            if (nowToken):
                return nowToken
            else:
                # 账号或密码错误
                return "444"
    else:
        print("token未设置")
        nowToken = login(phone, password)
        if (nowToken):
            return nowToken
        else:
            # 账号或密码错误
            return "444"






'''
作者：KKDAJ
功能：校验Token是否有效，Token进行其他操作不会挤掉
DateTime: 2020年12月5日00:19:56
'''
def istoken(token):
    planUrl = readJsonFile("../conf/urlMain.json")['planUrl']
    print(planUrl)
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
        print("Token可用，无需替换")
        return True
    elif (resp['code'] == 401):
        print("Token已过期，不可用")
        return False
    else:
        print("Token验证失败，程序异常" + resp['msg'])
        return
'''
作者：KKDAJ
功能：通过账号密码登陆，获取Token
DateTime: 2020年12月5日00:19:56
'''

def login(phone,password):
    data = {
        "phone": phone,
        "password": password,
        "loginType": "android"
    }
    resp = PostUrl(readJsonFile("../conf/urlMain.json")['loginUrl'], headers, data)
    if (resp['code']==200):
        print("登陆成功，获取到token")
        return resp["data"]["token"]
    else:
        print("登陆返回:"+resp)
        print("登陆失败，账号或密码错误")
        return False
