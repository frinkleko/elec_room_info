from .mail import EmailSender
from .pushplus import PushplusSender
from .wxpusher import WxpusherSender

class Sender:
    def __init__(self, config):
        self._config = config
        # 根据配置决定是否启用 EmailSender 和 PushplusSender 和 WxpusherSender
        self.email_sender = EmailSender(config=self._config) if self._config['email']['enable'] else None
        self.pushplus_sender = PushplusSender(config=self._config) if self._config['pushplus']['enable'] else None
        self.wxpusher_sender = WxpusherSender(config=self._config) if self._config['wxpusher']['enable'] else None
        self.to_emails = self._config['balance_monitor']['to_emails']

    def send(self, subject=None, message=None):
        if self.email_sender:
            self.email_sender.send_email(self.to_emails, subject, message)

        if self.pushplus_sender:
            self.pushplus_sender.send_push(subject, message)

        if self.wxpusher_sender:
            self.wxpusher_sender.send_push(subject, message)
