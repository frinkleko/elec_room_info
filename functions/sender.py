import requests
import json
import smtplib
from email.mime.text import MIMEText
from functions.utils import get_logger, Config

logger = get_logger(__name__)


class Sender:
    """
    Base Sender class to be extended for various notification mechanisms.
    """

    def send(self, subject, message):
        raise NotImplementedError("Extend this class to implement send functionality.")


class EmailSender(Sender):
    def send(self, subject, message):
        sender_email = Config.get("EMAIL_SENDER")
        receiver_email = Config.get(
            "BALANCE_MONITOR_RECEIVER_EMAIL", "default_receiver@example.com"
        )
        smtp_server = Config.get("EMAIL_SMTP_SERVER")
        smtp_port = Config.get("EMAIL_SMTP_PORT", 587)
        smtp_user = Config.get("EMAIL_SMTP_USER")
        smtp_password = Config.get("SMTP_PASSWORD")

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        try:
            with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(sender_email, [receiver_email], msg.as_string())
            logger.info("Email notification sent successfully!")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")


class PushplusSender(Sender):
    def send(self, subject, message):
        token = Config.get("PUSHPLUS_TOKEN")
        topic = Config.get("PUSHPLUS_TOPIC", "")
        channel = Config.get("PUSHPLUS_CHANNEL", "wechat")
        max_attempts = int(Config.get("PUSHPLUS_MAX_ATTEMPTS", 3))

        url = "https://www.pushplus.plus/send"
        headers = {"Content-Type": "application/json"}

        data = {
            "token": token,
            "title": subject,
            "content": message,
            "template": "markdown",
            "topic": topic,
            "channel": channel,
            "webhook": "",
        }

        for attempt in range(max_attempts):
            try:
                response = requests.post(url, headers=headers, json=data).json()
                if response.get("code") == 200:
                    logger.info("Pushplus message sent successfully!")
                    return
                else:
                    logger.error(f"Pushplus message failed: {response}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Pushplus request error: {e}, attempt {attempt + 1}")

        logger.error("Pushplus sending failed after maximum attempts!")


class WxpusherSender(Sender):
    """
    Wxpusher message sender class for sending notifications to user devices or topic groups.
    """

    def send(self, subject, message):
        spt = Config.get("WXPUSHER_SPT")
        app_token = Config.get("WXPUSHER_APP_TOKEN")
        topic_ids = Config.get("WXPUSHER_TOPIC_IDS", "").split(
            ","
        )  # Ensure comma-separated topic IDs
        max_attempts = int(Config.get("WXPUSHER_MAX_ATTEMPTS", 3))

        headers = {"Content-Type": "application/json"}

        if spt:
            # Push to individual using SPT
            url = "https://wxpusher.zjiecode.com/api/send/message/simple-push"
            data = {
                "content": message,
                "summary": subject,
                "contentType": 1,
                "spt": spt,
            }
            self._send_post(url, data, headers)

        if app_token and topic_ids:
            # Push to topic groups using App Token
            url = "https://wxpusher.zjiecode.com/api/send/message"
            data = {
                "appToken": app_token,
                "content": message,
                "summary": subject,
                "contentType": 1,
                "topicIds": topic_ids,
                "verifyPayType": 0,
            }
            self._send_post(url, data, headers)

    def _send_post(self, url, data, headers):
        for attempt in range(int(Config.get("WXPUSHER_MAX_ATTEMPTS", 3))):
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(data), timeout=10
                ).json()
                if response.get("code") == 1000:
                    logger.info("Wxpusher message sent successfully!")
                    return
                else:
                    logger.error(f"Wxpusher message failed: {response}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Wxpusher request error: {e}, attempt {attempt + 1}")

        logger.error("Wxpusher sending failed after maximum attempts!")


class TelegramSender(Sender):
    """
    Telegram Bot sender class for sending notifications.
    """

    def send(self, subject, message):
        bot_token = Config.get("TELEGRAM_BOT_TOKEN")
        chat_id = Config.get("TELEGRAM_CHAT_ID")
        max_attempts = int(Config.get("TELEGRAM_MAX_ATTEMPTS", 3))

        if not bot_token or not chat_id:
            logger.warning("Telegram bot token or chat ID is not configured.")
            return

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        headers = {"Content-Type": "application/json"}

        data = {
            "chat_id": chat_id,
            "text": f"📢 {subject}\n\n{message}",
        }

        for attempt in range(max_attempts):
            try:
                response = requests.post(url, headers=headers, json=data).json()
                if response.get("ok"):
                    logger.info("Telegram message sent successfully!")
                    return
                else:
                    logger.error(f"Telegram message failed: {response}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Telegram request error: {e}, attempt {attempt + 1}")

        logger.error("Telegram sending failed after maximum attempts!")


class MockSender(Sender):
    """
    Mock sender for debugging and testing.
    """

    def send(self, subject, message):
        logger.info(f"[MOCK] Subject: {subject}")
        logger.info(f"[MOCK] Message: {message}")
