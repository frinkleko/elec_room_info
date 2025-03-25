import json
import requests

from elec_room_info.utils.log import get_logger
logger = get_logger(__name__)


class WxpusherSender:
    def __init__(self, config):
        self._config = config
        self._spt = self._config['wxpusher']['spt']
        self._max_attempts = self._config['pushplus']['max_attempts']

    def send_push(self, subject = None, message = None):
        url = 'https://wxpusher.zjiecode.com/api/send/message/simple-push'
        headers = {'Content-Type': 'application/json'}

        data = {
            # 推送内容，必传
            "content":f"{message}",
            # "content":"<h1>极简推送</h1><br/><p style=\"color:red;\">欢迎你使用WxPusher，推荐使用HTML发送</p>",
            # 消息摘要，显示在微信聊天页面或者模版消息卡片上，限制长度20(微信只能显示20)，可以不传，不传默认截取content前面的内容。
            "summary":f"{subject}",
            # 内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签，推荐使用这种) 3表示markdown 
            "contentType":1,
            # 发送SPT，如果发送给一个用户，直接传simplePushToken就行了，不用传simplePushTokenList
            "spt":self._spt,
            # 发送SPT，如果发送给多个用户，只传simplePushTokenList即可，请注意，【这是一个数组】！！，最多不能超过10个
            # "sptList":["SPT_xx1","SPT_xx2"],
            # 原文链接，可选参数
            # "url":"https://wxpusher.zjiecode.com",
        }

        for attempt in range(self._max_attempts):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10).json()

                if response.get('code') == 1000:
                    logger.debug('Wxpusher 消息推送成功！')
                    return
                else:
                    logger.error(f'Wxpusher 消息推送失败: {response}')
                    continue

            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常：{e}，第 {attempt + 1} 次尝试")
        
        logger.error(f"尝试次数已达最大值，Wxpusher 推送失败!")
