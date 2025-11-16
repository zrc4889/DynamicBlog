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
    message.attach(MIMEText("Nothing", "plain"))
    
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
for key, val in data.items():
    s = s + '中午好，今天是编号' + str((val - today).days) + '天。'
day = (val - today).days
send(s)

