
import requests
import json
import smtplib
import threading
from email.mime.text import MIMEText
from email.utils import formataddr


def getStockPrice(stock):
     url = "https://gupiao.baidu.com/tpl/betsInfo?code="+stock;
     response  = requests.get(url)
     print(response.content)
     text = json.loads(response.content)
     return [text['close'],text['html']]

def mail(email,mailContent):
    config = read_config("mail_config.json")
    sender = config["sender"]    # 发件人邮箱账号
    mail_pass = config["pass"]              # 发件人邮箱密码(当时申请smtp给的口令)
    my_user = email      # 收件人邮箱账号，我这边发送给自己
    ret=True
    try:
        msg=MIMEText(mailContent[0],'html','utf-8')
        msg['From']=formataddr([sender,sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr([email,my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="股票提醒"+ mailContent[1]              # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(sender, mail_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()# 关闭连接
    except Exception:# 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret

def warn(stock,min_price,email):
    try:
        response = getStockPrice(stock)
        price = response[0]
        mailContent = [response[1],price]
        #print(mailContent[0])
        if (float(price)<=min_price) :
            ret = mail(email,mailContent)
    except Exception as e:
        print(e)

def read_config(fileName):
    with open(fileName,encoding='utf-8') as f:
        pop_data = json.load(f)
    return pop_data


def threading_warn():
    with open("config.json",encoding='utf-8') as f:
        pop_data = json.load(f)

        for pop_dict in pop_data:
            stock = pop_dict['stock']
            min_price = pop_dict['min_price']
            email = pop_dict['email']
            warn(stock,min_price,email)



    timer = threading.Timer(30,threading_warn)
    timer.start()

if __name__=="__main__":
    # data = read_config("mail_config.json")
    # print(data["sender"])
    threading_warn()
