
import requests
import json
import smtplib
import threading
from email.mime.text import MIMEText
from email.utils import formataddr


def getStockPrice(stock):
     url = "https://gupiao.baidu.com/tpl/betsInfo?code="+stock;
     response  = requests.get(url)
     #print(response.content)
     text = json.loads(response.content)
     return [text['close'],text['html']]

def mail(email,mailContent):
    my_sender = '573631001@qq.com'    # 发件人邮箱账号
    my_pass = 'ukxsyqakygzvbcia'              # 发件人邮箱密码(当时申请smtp给的口令)
    my_user = email      # 收件人邮箱账号，我这边发送给自己
    ret=True
    try:
        msg=MIMEText(mailContent[0],'html','utf-8')
        msg['From']=formataddr(["573631001@qq.com",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr([email,my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="股票提醒"+ mailContent[1]              # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
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


def threading_warn():
    warn("sh600392",15.5,'510645436@qq.com')
    warn("sz000786",24.2,'510645436@qq.com')
    warn("sz002743",8,'510645436@qq.com')
    warn("sz002223",22,'510645436@qq.com')
    warn("sh600581",12.4,'510645436@qq.com')
    warn("sh603139",23.4,'510645436@qq.com')


    timer = threading.Timer(30,threading_warn)
    timer.start()

if __name__=="__main__":
    print("main")
    #getStockPrice("sh600392")
    #mail('510645436@qq.com')
    threading_warn()
