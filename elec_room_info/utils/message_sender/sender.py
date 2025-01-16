from .mail import EmailSender
from .pushplus import PushplusSender


class Sender:
    def __init__(self, config):
        self._config = config
        # 根据配置决定是否启用 EmailSender 和 PushplusSender
        self.email_sender = EmailSender(config=self._config) if self._config['email']['enable'] else None
        self.pushplus_sender = PushplusSender(config=self._config) if self._config['pushplus']['enable'] else None
        self.to_emails = self._config['balance_monitor']['to_emails']

    def send(self, subject=None, message=None):
        if self.email_sender:
            self.email_sender.send_email(self.to_emails, subject, message)

        if self.pushplus_sender:
            self.pushplus_sender.send_push(subject, message)
