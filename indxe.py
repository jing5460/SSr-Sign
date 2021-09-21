# -*- coding: utf-8 -*-
"""
@Time ： 2020/9/15 9:52
@Auth ： Ne-21
@Des : sspanel自动每日签到脚本
@File ：sspanel_qd.py
@IDE ：PyCharm
@Motto：Another me.
sspanel自动每日签到脚本，基于项目https://github.com/zhjc1124/ssr_autocheckin修改
"""
import requests
import re

requests.packages.urllib3.disable_warnings()

class SspanelQd(object):
    def __init__(self):
        ###############登录信息配置区###############
        # 机场地址
        self.base_url = 'https://*****link'
        # 登录信息
        self.email = '******@qq.com'
        self.password = '******'
        ###########################################
        ##############推送渠道配置区###############
        # Server酱推送
        self.sckey = ''
        # 酷推qq推送
        self.ktkey = ''
        # ServerTurbo推送
        self.SendKey = ''
        # Qmsg私聊推送
        self.QmsgKey = ''
        # Telegram私聊推送
        self.tele_api_url = 'https://api.telegram.org'
        self.tele_bot_token = ''
        self.tele_user_id = ''
        # Pushplus私聊推送
        self.push_token = ''
        ##########################################

    def checkin(self):
        email = self.email.split('@')
        email = email[0] + '%40' + email[1]
        password = self.password
        try:
            session = requests.session()
            session.get(self.base_url, verify=False)

            login_url = self.base_url + '/auth/login'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }

            post_data = 'email=' + email + '&passwd=' + password + '&code='
            post_data = post_data.encode()
            session.post(login_url, post_data, headers=headers, verify=False)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Referer': self.base_url + '/user'
            }

            response = session.post(self.base_url + '/user/checkin', headers=headers, verify=False)
            # print(response.text)
            msg = (response.json()).get('msg')
            print(msg)
        except:
            return False

        info_url = self.base_url + '/user'
        response = session.get(info_url, verify=False)
        """
        以下只适配了editXY主题
        """
        try:
            level = re.findall(r'\["Class", "(.*?)"],', response.text)[0]
            day = re.findall(r'\["Class_Expire", "(.*)"],', response.text)[0]
            rest = re.findall(r'\["Unused_Traffic", "(.*?)"]', response.text)[0]
            msg = "- 今日签到信息："+str(msg)+"\n- 用户等级："+str(level)+"\n- 到期时间："+str(day)+"\n- 剩余流量："+str(rest)
            print(msg)
            return msg
        except:
            return msg

    #Qmsg私聊推送
    def Qmsg_send(self, msg):
        if self.QmsgKey == '':
            return
        qmsg_url = 'https://qmsg.zendee.cn/send/' + str(self.QmsgKey)
        data = {
            'msg': msg,
        }
        requests.post(qmsg_url, data=data)

    # Server酱推送
    def server_send(self, msg):
        if self.SendKey == '':
            return
        server_url = "https://sctapi.ftqq.com/" + str(self.SendKey) + ".send"
        data = {
                'text': "今日的流量白嫖到啦！",
                'desp': msg
            }
        requests.post(server_url, data=data)

    # 酷推QQ推送
    def kt_send(self, msg):
        if self.ktkey == '':
            return
        kt_url = 'https://push.xuthus.cc/send/'+str(self.ktkey)
        data = ('签到完成，点击查看详细信息~\n'+str(msg)).encode("utf-8")
        requests.post(kt_url, data=data)

    # Server酱推送
    def serverTurbo_send(self, msg):
        if self.sckey == '':
            return
        server_url = "https://sc.ftqq.com/" + str(self.sckey) + ".send"
        data = {
            'text': "签到完成，点击查看详细信息~",
            'desp': msg
        }
        requests.post(server_url, data=data)
        
    def tele_send(self, msg: str):
        if self.tele_bot_token == '':
            return
        tele_url = f"{self.tele_api_url}/bot{self.tele_bot_token}/sendMessage"
        data = {
            'chat_id': self.tele_user_id,
            'parse_mode': "Markdown",
            'text': msg
        }
        requests.post(tele_url, data=data)
        
    # Pushplus推送
    def pushplus_send(self,msg):
        if self.push_token == '':
            return
        token = self.push_token 
        title= '机场签到通知'
        content = msg
        url = 'http://www.pushplus.plus/send'
        data = {
            "token":token,
            "title":title,
            "content":content
            }
        body=json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type':'application/json'}
        requests.post(url,data=body,headers=headers)
   

    def main(self):
        msg = self.checkin()
        if msg == False:
            print("网址不正确或网站禁止访问。")
        else:
            self.server_send(msg)
            self.kt_send(msg)
            self.serverTurbo_send(msg)
            self.Qmsg_send(msg)

# 云函数入口
def main_handler(event, context):
    run = SspanelQd()
    run.main()

if __name__ == '__main__':
    run = SspanelQd()
    run.main()
