const nodemailer = require('nodemailer');
const fs = require('fs');

async function sendEmail(config) {
  // 创建邮件传输器
  const transporter = nodemailer.createTransporter({
    host: config.smtpHost,
    port: config.smtpPort,
    secure: config.secure, // true for 465, false for other ports
    auth: {
      user: config.smtpUser,
      pass: config.smtpPass
    }
  });

  // 邮件内容
  const mailOptions = {
    from: `"网页截图服务" <${config.fromEmail}>`,
    to: config.toEmail,
    subject: config.subject || '网页截图报告',
    html: `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #333;">网页截图报告</h2>
        <p><strong>目标网址:</strong> ${config.url}</p>
        <p><strong>截图时间:</strong> ${new Date().toLocaleString('zh-CN')}</p>
        <p>这是自动生成的网页截图，请查收附件。</p>
        <hr style="border: none; border-top: 1px solid #eee;">
        <p style="color: #666; font-size: 12px;">
          此邮件由 GitHub Actions 自动发送
        </p>
      </div>
    `,
    attachments: config.attachments
  };

  try {
    const info = await transporter.sendMail(mailOptions);
    console.log('Email sent successfully:', info.messageId);
    return info;
  } catch (error) {
    console.error('Error sending email:', error);
    throw error;
  }
}

// 主函数
async function main() {
  const config = {
    smtpHost: process.env.SMTP_HOST,
    smtpPort: parseInt(process.env.SMTP_PORT || '587'),
    secure: process.env.SMTP_SECURE === 'true',
    smtpUser: process.env.SMTP_USER,
    smtpPass: process.env.SMTP_PASS,
    fromEmail: process.env.FROM_EMAIL,
    toEmail: process.env.TO_EMAIL,
    url: process.env.WEBPAGE_URL,
    subject: process.env.EMAIL_SUBJECT || '网页截图报告'
  };

  // 查找最新的截图文件
  const screenshotsDir = './screenshots';
  let latestScreenshot = null;

  if (fs.existsSync(screenshotsDir)) {
    const files = fs.readdirSync(screenshotsDir)
      .filter(file => file.endsWith('.jpg') || file.endsWith('.png'))
      .map(file => ({
        name: file,
        time: fs.statSync(`${screenshotsDir}/${file}`).mtime.getTime()
      }))
      .sort((a, b) => b.time - a.time);

    if (files.length > 0) {
      latestScreenshot = `${screenshotsDir}/${files[0].name}`;
    }
  }

  if (!latestScreenshot) {
    throw new Error('No screenshot found to send');
  }

  config.attachments = [
    {
      filename: `screenshot-${new Date().toISOString().split('T')[0]}.jpg`,
      path: latestScreenshot
    }
  ];

  try {
    await sendEmail(config);
    console.log('Email sent successfully');
  } catch (error) {
    console.error('Failed to send email:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = sendEmail;
