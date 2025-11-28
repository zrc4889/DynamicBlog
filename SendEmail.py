import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 发件人和收件人信息
sender_email = "zrc_4889@163.com"
receiver_email = "zrc4889@163.com"
password = "ZASRS37tuwxerHBZ"

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
send('自证是最大的陷阱，诬告你的人就是要让你陷入自证陷阱，因为她知道你什么都没干，你自证她也不会承认，所以千万不要陷入自证陷阱。最好的方法是谁主张谁举证，把锅甩到别人身上，还有就是千万不要道歉或者认错，人做错了事才会道歉和认错，你什么都没做，道什么歉认什么错。不要被别人的咄咄逼人的态度压住，自己没做错事就昂首挺胸拿出气势来压倒别人，就和视频里表现的一样。')

