import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

from .log import get_logger
logger = get_logger(__name__)


class EmailSender:
    def __init__(self, **kwargs):
        self._config = kwargs['config']

        self._SENDER_EMAIL = self._config['email']['sender_email']
        self._SENDER_NAME = self._config['email']['sender_name']
        self._SMTP_SERVER = self._config['email']['smtp_server']
        self._SMTP_PORT = self._config['email']['smtp_port']
        self._SMTP_USER = self._config['email']['smtp_user']
        self._SMTP_PASSWORD = self._config['email']['smtp_password']

        # self._SENDER_EMAIL = kwargs['SENDER_EMAIL']
        # self._SENDER_NAME = kwargs.get('SENDER_NAME', 'root')
        # self._SMTP_SERVER = kwargs['SMTP_SERVER']
        # self._SMTP_PORT = kwargs.get('SMTP_PORT', 587)
        # self._SMTP_USER = kwargs['SMTP_USER']
        # self._SMTP_PASSWORD = kwargs['SMTP_PASSWORD']

    def send_email(self, recipient_email, subject, message):
        msg = MIMEMultipart()
        msg['From'] = formataddr((self._SENDER_NAME, self._SENDER_EMAIL))
        msg['To'] = recipient_email
        msg['Subject'] = subject

        body = message
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        try:
            with smtplib.SMTP(self._SMTP_SERVER, self._SMTP_PORT) as server:
                server.starttls()  # 启用TLS加密
                server.login(self._SMTP_USER, self._SMTP_PASSWORD)  # 登录SMTP服务器
                server.sendmail(self._SENDER_EMAIL, recipient_email, msg.as_string())
            # print(f"邮件已发送至 {recipient_email}")
            logger.debug(f"邮件已发送至 {recipient_email}")
        except Exception as e:
            # print(f"发送邮件时出错: {e}")
            logger.error(f"发送邮件时出错: {e}")


# 示例用法
if __name__ == "__main__":
    TEST_CONFIG = {
        'SENDER_EMAIL': '3265168281@qq.com',
        'SENDER_NAME': 'root',
        'SMTP_SERVER': 'smtp.qq.com',
        'SMTP_PORT': 587,
        'SMTP_USER': '3265168281@qq.com',
        'SMTP_PASSWORD': 'xzcedkulvpqfcjbi'
    }
    recipient = '3265168281@qq.com'  # 接收邮件的邮箱地址
    subject = '系统提醒'
    message = '这是一封系统提醒邮件。'

    email_sender = EmailSender(**TEST_CONFIG)
    email_sender.send_email(recipient, subject, message)
