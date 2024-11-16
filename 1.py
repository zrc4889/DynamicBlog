import zmail

mail = {
    'subject': 'Python - Zmail!',  # 邮件标题
    'content_text': 'This message from zmail!',  # 邮件内容
}

server = zmail.server('zrc_4889@163.com', 'ZASRS37tuwxerHBZ')

server.send_mail('zrc4889@163.com', mail)
