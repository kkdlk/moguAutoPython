from utils.UtilsClass import readJsonFile
import random


'''
根据专业随机生成日报内容
'''
def randDayTxt (leableati,itemc):
    dayTxt = readJsonFile("../db/day/"+leableati+"_Day.json")['data']
    dayTxtleanth = random.randint(0, len(dayTxt))
    contxt = ''
    for i in range(0,itemc):
        contxt+=dayTxt[dayTxtleanth]['txt']
        # print(contxt)
    return contxt


'''
   根据当前周随机生成周报内容 (当前第几周)
'''

def randWeekTxt(nowWeekItem):
    weekthis= random.randint(1, 2)
    week1 = readJsonFile("../db/week/week1.json")['data']
    week2 = readJsonFile("../db/week/week2.json")['data']
    if (weekthis==1):
        return week1[int(nowWeekItem-1)]['txt'] #因为角标从0开始 最小为1 所以-1
    else:
        return week2[int(nowWeekItem-1)]['txt']

