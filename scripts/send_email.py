#!/usr/bin/env python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import glob
from datetime import datetime

class EmailSender:
    def __init__(self, config):
        self.config = config
    
    def find_latest_screenshot(self):
        """查找最新的截图文件"""
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            raise FileNotFoundError(f"截图目录不存在: {screenshot_dir}")
        
        # 查找所有图片文件
        image_files = glob.glob(os.path.join(screenshot_dir, "*.png")) + \
                     glob.glob(os.path.join(screenshot_dir, "*.jpg")) + \
                     glob.glob(os.path.join(screenshot_dir, "*.jpeg"))
        
        if not image_files:
            raise FileNotFoundError("未找到截图文件")
        
        # 按修改时间排序，获取最新的文件
        latest_file = max(image_files, key=os.path.getmtime)
        return latest_file
    
    def create_email_content(self, url):
        """创建邮件内容"""
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
                .content {{ margin: 20px 0; }}
                .footer {{ color: #666; font-size: 12px; margin-top: 20px; padding-top: 10px; border-top: 1px solid #eee; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>📸 网页截图报告</h2>
            </div>
            <div class="content">
                <p><strong>🌐 目标网址:</strong> {url}</p>
                <p><strong>⏰ 截图时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>这是自动生成的网页截图，请查收附件。</p>
            </div>
            <div class="footer">
                <p>此邮件由 GitHub Actions 自动发送</p>
            </div>
        </body>
        </html>
        """
        return html_content
    
    def send_email(self, url):
        """发送邮件"""
        try:
            # 查找最新的截图
            screenshot_path = self.find_latest_screenshot()
            print(f"找到截图文件: {screenshot_path}")
            
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = self.config['from_email']
            msg['To'] = self.config['to_email']
            msg['Subject'] = self.config.get('subject', f'网页截图报告 - {url}')
            
            # 添加邮件正文
            html_content = self.create_email_content(url)
            msg.attach(MIMEText(html_content, 'html'))
            
            # 添加附件
            with open(screenshot_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            filename = f"screenshot-{datetime.now().strftime('%Y%m%d')}.jpg"
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            msg.attach(part)
            
            # 发送邮件
            print("正在连接邮件服务器...")
            if self.config['secure']:
                # 使用 SSL
                server = smtplib.SMTP_SSL(self.config['smtp_host'], self.config['smtp_port'])
            else:
                # 使用 TLS
                server = smtplib.SMTP(self.config['smtp_host'], self.config['smtp_port'])
                server.starttls()
            
            # 登录
            server.login(self.config['smtp_user'], self.config['smtp_pass'])
            
            # 发送邮件
            text = msg.as_string()
            server.sendmail(self.config['from_email'], self.config['to_email'], text)
            server.quit()
            
            print("邮件发送成功!")
            return True
            
        except Exception as e:
            print(f"邮件发送失败: {e}")
            raise e

def main():
    """主函数"""
    # 从环境变量获取配置
    config = {
        'smtp_host': 'stmp.163.com',
        'smtp_port': '587',
        'smtp_user': 'zrc_4889@163.com',
        'smtp_pass': 'ZASRS37tuwxerHBZ',
        'from_email': 'zrc_4889@163.com',
        'to_email': 'zrc4889@163.com',
        'subject': '网页截图报告'
    }
    
    url = os.getenv('WEBPAGE_URL', 'https://github.com')
    
    # 检查必要配置
    required_fields = ['smtp_host', 'smtp_user', 'smtp_pass', 'from_email', 'to_email']
    for field in required_fields:
        if not config[field]:
            raise ValueError(f"缺少必要的环境变量: {field}")
    
    # 发送邮件
    sender = EmailSender(config)
    sender.send_email(url)

if __name__ == "__main__":
    main()
