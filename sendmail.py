#-*-coding:utf-8-*-  

#===============================================================================
# 导入smtplib和MIMEText
#===============================================================================
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import base64

_user='573631001@qq.com'    # 发件地址
_pwd="kwtmqodjdaswbdib"
_smtp="smtp.qq.com"


def send_mail(_to,attFile):
    msg = MIMEMultipart()
    body = MIMEText(attFile, 'HTML', 'utf-8')#邮件内容
    msg['Subject'] = Header("交易量数据", 'utf-8')#邮件的标题
    msg['From'] = _user
    msg['To'] = _to
    msg.attach(body)
    #
    #
    #添加附件
    att=MIMEText(open(attFile,"rb").read(),"base64","utf-8")#打开附件地址
    att["Content-Type"] = "application/octet-stream"
    # att["Content-Disposition"] ='attachment;filename=%s' % attFile.encode('gb2312')
    att.add_header('Content-Disposition', 'attachment', filename=('gb2312', '', attFile))

    msg.attach(att)

    #
    #
    #发送邮件
    s = smtplib.SMTP_SSL(_smtp)
    # s.set_debuglevel(1)
    s.login(_user,_pwd)  # 登录邮箱的账户和密码
    s.sendmail(_user,_to, msg.as_string())#发送邮件
    s.quit()
    print("邮件发送成功")

if __name__=="__main__":
    _to="510645436@qq.com"      # 收件人地址，多人以分号分隔
    send_mail(_to,'example.csv')
