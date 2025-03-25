import json
import requests

from elec_room_info.utils.log import get_logger
logger = get_logger(__name__)


class WxpusherSender:
    def __init__(self, config):
        self._config = config
        self._spt = self._config['wxpusher']['spt']
        self._app_token = self._config['wxpusher']['app_token']
        self._topic_ids = list(self._config['wxpusher']['topic_ids'])
        self._max_attempts = self._config['wxpusher']['max_attempts']

    def send_push(self, subject = None, message = None):
        headers = {'Content-Type': 'application/json'}
        if self._spt is not None and self._spt != '':
            logger.info('Wxpusher 推送 SPT 已配置')
            url = 'https://wxpusher.zjiecode.com/api/send/message/simple-push'
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
            self.send_post(url, data, headers)
        if self._app_token is not None and self._app_token != '' and len(self._topic_ids) > 0:
            logger.info('Wxpusher 推送 APP Token 已配置')
            url = 'https://wxpusher.zjiecode.com/api/send/message'
            data = {
                "appToken":self._app_token,  # 必传
                "content":f"{message}",  # 必传
                # 消息摘要，显示在微信聊天页面或者模版消息卡片上，限制长度20(微信只能显示20)，可以不传，不传默认截取content前面的内容。
                "summary":f"{subject}",
                # 内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签，推荐使用这种) 3表示markdown 
                "contentType":1,
                # 发送目标的topicId，是一个数组！！！，也就是群发，使用uids单发的时候， 可以不传。
                "topicIds":self._topic_ids,
                # 发送目标的UID，是一个数组。注意uids和topicIds可以同时填写，也可以只填写一个。
                # "uids":[
                #     "UID_xxxx"
                # ],
                # 原文链接，可选参数
                # "url":"https://wxpusher.zjiecode.com", 
                # 是否验证订阅时间，true表示只推送给付费订阅用户，false表示推送的时候，不验证付费，不验证用户订阅到期时间，用户订阅过期了，也能收到。
                # verifyPay字段即将被废弃，请使用verifyPayType字段，传verifyPayType会忽略verifyPay
                # "verifyPay":false, 
                # 是否验证订阅时间，0：不验证，1:只发送给付费的用户，2:只发送给未订阅或者订阅过期的用户
                "verifyPayType":0 
            }
            self.send_post(url, data, headers)



    def send_post(self, url, data, headers):

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
