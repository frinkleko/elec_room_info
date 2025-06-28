# Sender 参数配置

本页介绍了支持的 Sender 类型及其参数配置，最后介绍了自定义 Sender 的方式。

## **支持的 Sender 类型**

### **1. Pushplus**
- 参数说明：
  | 参数名称         | 类型   | 描述                             |
  | ---------------- | ------ | -------------------------------- |
  | `PUSHPLUS_TOKEN` | string | PushPlus API Token，用于认证推送 |

- 示例配置：
```yaml
PUSHPLUS_TOKEN: YourTokenHere
```

---

### **2. Wxpusher**
- 参数说明：
  | 参数名称             | 类型   | 描述                                    |
  | -------------------- | ------ | --------------------------------------- |
  | `WXPUSHER_APP_TOKEN` | string | 获取自 Wxpusher 的 APP Token            |
  | `WXPUSHER_TOPIC_IDS` | list   | 推送的群组 ID，可通过 Wxpusher 官网获取 |

- 示例配置：
```yaml
WXPUSHER_APP_TOKEN: YourAppTokenHere
WXPUSHER_TOPIC_IDS: ["1234", "5678"]
```

---

### **3. Telegram Bot**
- 参数说明：
  | 参数名称             | 类型   | 描述                      |
  | -------------------- | ------ | ------------------------- |
  | `TELEGRAM_BOT_TOKEN` | string | Telegram Bot 的 API Token |
  | `TELEGRAM_CHAT_ID`   | string | Telegram 接收者的 chat ID |

- 示例配置：
```yaml
TELEGRAM_BOT_TOKEN: YourBotTokenHere
TELEGRAM_CHAT_ID: YourChatIdHere
```

---

### **4. Email**
- 参数说明：
  | 参数名称            | 类型   | 描述                 |
  | ------------------- | ------ | -------------------- |
  | `EMAIL_SENDER`      | string | 发件人邮箱地址       |
  | `EMAIL_SMTP_SERVER` | string | SMTP 服务器地址      |
  | `EMAIL_SMTP_PORT`   | int    | SMTP 端口 (例如 587) |
  | `SMTP_PASSWORD`     | string | 邮箱 SMTP 认证密码   |

- 示例配置：
```yaml
EMAIL_SENDER: your_email@example.com
EMAIL_SMTP_SERVER: smtp.example.com
EMAIL_SMTP_PORT: 587
SMTP_PASSWORD: YourPasswordHere
```

## 自定义 Sender

你只需要继承`functions\sender.py`中的基类并定义send方法即可。然后在Send_Type指定你的基类名字，并且修改`.main.py`中的`Sender`导入。

以Email为例
```python
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
```
