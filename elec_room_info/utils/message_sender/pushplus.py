import json
import requests

from elec_room_info.utils.log import get_logger
logger = get_logger(__name__)


class PushplusSender:
    def __init__(self, config):
        self._config = config
        self._token = self._config['pushplus']['token']
        self._topic = self._config['pushplus']['topic']
        self._channel = self._config['pushplus']['channel']
        self._max_attempts = self._config['pushplus']['max_attempts']

    def send_push(self, subject = None, message = None):
        url = 'https://www.pushplus.plus/send'
        headers = {'Content-Type': 'application/json'}

        data = {
            "token": self._token,
            "title": subject,
            "content": message,
            "template": "markdown",
            "topic": self._topic,
            "channel": self._channel,
            "webhook": ""
        }

        for attempt in range(self._max_attempts):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10).json()

                if response.get('code') == 200:
                    logger.debug('Pushplus 消息推送成功！')
                    return
                else:
                    logger.error(f'Pushplus 消息推送失败: {response}')
                    continue

            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常：{e}，第 {attempt + 1} 次尝试")
        
        logger.error(f"尝试次数已达最大值，Pushplus 推送失败!")
