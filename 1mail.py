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
        '2027 全国高考': datetime.date(2027, 6, 7)
    }
s = s + 'CharonTree要去去哈工大踢雪地足球。'
for key, val in data.items():
    s = s + '距离' + str(key) + '还有' + str((val - today).days) + '天。'
day = (val - today).days
s = s + '不要以为时间还很多，仅剩' + str(floor(day / 7)) + '周'
    
send(s)

