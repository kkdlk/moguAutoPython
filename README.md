## 声明

蘑菇丁自动登录，自动签到，日报，周报，月报填写,支持批量导入信息和自定义信息

优化了信息提示模块；

添加了Token过期，自动签到，自动生成日报信息，自动生成周报信息，自动生成月报信息，等模块

添加了各个模块的注释，和简单异常的处理
---------------------------------
## 相关参数和注意事项

```
{
  "RootSckey":"管理员的Server酱秘钥，http://sc.ftqq.com/3.version",
  "loginData": [
     {
      "kkdaj": "内容",
      "phone": "蘑菇丁账号",
      "password": "蘑菇丁密码",
      "sckey": "server酱密钥，可为空",
      "token": "蘑菇钉token，可为空",
      "leableati": "专业 C、CESHI、CHUDENGJIAOYU、HULI、JAVA、KUAIJI、WULIUGUANLI、XUEQIANJIAOYU、YAOXUE、",
      "startWeekTime": "周报开始时间（计算当前周是第几周）",
      "province": "市",
      "city": "区",
      "address": "地址",
      "longitude": "经度",
      "latitude": "纬度",
      "signOnDate": "上班打卡时间（每天几点打上班卡24小时制）",
      "signOutDate": "下班打卡时间（每天几点打下班卡24小时制）",
      "daySign": "日报时间（每天几点填写日报，24小时制）",
      "weekDate":"每周周报时间（周几填写周报）数字1-7代表周一到周日",
      "monthDate":"每月月报时间（每月几号填写月报）数字1-29/1-30/1-31",
      "endSign": "彻底结束本次服务的时间2020-12-06"
    }
  ]
}

```
### 注意事项

context文件夹中 main.json是配置批量导入账号信息的、文件夹中其他文件是各专业的日报月报周报信息

账号信息不可重复添加，重复添加会进行多次打卡！！！！！！！！！！切记

---------------------------------

## 静态配置的Jenkinsfile

````
pipeline {
  agent any
  stages {
    stage('检出') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: GIT_BUILD_REF]],
          userRemoteConfigs: [[
            url: GIT_REPO_URL,
            credentialsId: CREDENTIALS_ID
          ]]])
        }
      }
      stage('安装环境') {
        steps {
          sh '''yarn install
cd ./src
node main.js'''
        }
      }
    }
  }
````