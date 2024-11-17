import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def text():
    today = datetime.date.today()
    past_date = datetime.date(2025, 1, 1)
    delta = today - past_date
    return '距离新年还有 ' + delta + ' 天，加油！'

# 发件人和收件人信息
sender_email = "zrc_4889@163.com"
receiver_email = "zrc4889@163.com"
password = "ZASRS37tuwxerHBZ"
# password = os.environ['PASSWORD']

# 创建邮件
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = text()

# 添加邮件正文
message.attach(MIMEText("111", "plain"))

# 连接到SMTP服务器
with smtplib.SMTP("smtp.163.com", 25) as server:
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

# print("邮件已发送成功！")
