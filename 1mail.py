import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 发件人和收件人信息
sender_email = "zrc_4889@163.com"
receiver_email = "zrc4889@163.com"
password = "ZASRS37tuwxerHBZ"
# password = os.environ['PASSWORD']

def send(s):
    # 创建邮件
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = s
    
    # 添加邮件正文
    message.attach(MIMEText("111", "plain"))
    
    # 连接到SMTP服务器
    with smtplib.SMTP("smtp.163.com", 25) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    
    # print("邮件已发送成功！")

today = datetime.date.today()
s = ''
data = {
        '高一上福州市质检': datetime.date(2025, 1, 18),
        '2027 全国高考': datetime.date(2027, 6, 7)
    }
s = s + '我想去哈工大踢雪地足球。第一我只要你健康快乐，第二不要拿过去惩罚自己，第三做正确的事。'
for key, val in data.items():
    s = s + '距离' + str(key) + '还有' + str((val - today).days) + '天。'
    
send(s)

