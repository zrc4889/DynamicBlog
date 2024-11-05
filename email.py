import PyEmail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 发件人和收件人信息
sender_email = "zrc_4889@163.com"
receiver_email = "zrc4889@163.com"
password = "ZASRS37tuwxerHBZ"

# 创建邮件
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "欢迎回家！"

# 添加邮件正文
message.attach(MIMEText("正文。", "plain"))

# 连接到SMTP服务器
with smtplib.SMTP("smtp.163.com", 25) as server:
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

# print("邮件已发送成功！")
