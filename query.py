import random
import requests
from datetime import datetime
from utils.record_csv import CSVRecordHandler

from utils.config import Config

from utils.log import get_logger
logger = get_logger(__name__)


def create_query_form_data(info_json):
    aids = ['0030000000004901', '0030000000011101', '0030000000011201']
    aid = aids[eval(info_json['type'])]
    area = '{"area":"","areaname":""}'
    building = (f'{{"building":"{info_json["building"].split("&&&")[0]}","buildingid":'
                f'"{info_json["building"].split("&&&")[1]}"}}')
    floor = f'{{"floor":"{info_json["floor"].split("&&&")[0]}","floorid":"{info_json["floor"].split("&&&")[1]}"}}'
    room = f'{{"room":"{info_json["room"].split("&&&")[0]}","roomid":"{info_json["room"].split("&&&")[1]}"}}'
    return {
        'aid': aid,
        'area': area,
        'building': building,
        'floor': floor,
        'room': room
    }


def create_url(api_name):
    v = random.randint(1, 100)  # 生成1到100的随机整数
    return f'https://weixinchongzhi.scut.edu.cn/wechat/{api_name}.html?v={v}'


class ElecRoomQuery:
    """
    宿舍水电空调余额查询类
    """
    def __init__(self, **kwargs):
        """
        :param kwargs: 'session_id': 浏览器会话cookie, 'auth_link': 企业微信学生一卡通应用链接, 'csv_file_path': csv文件保存路径
        """
        self._config: Config = kwargs.get('config')

        self._session = self._config['query']['session_id']
        # self._auth_link = self._config['query']['auth_link']

        # self._session = kwargs.get('session_id', None)
        # self._auth_link = kwargs.get('auth_link', None)

        # if self._session == '' and self._auth_link == '':
        #     logger.error('ElecRoomQuery needs session_id or auth_link')
        #     raise ValueError('ElecRoomQuery needs session_id or auth_link')
        if self._session == '':
            while self._session == '':
                self._auth_link = input('input auth link: ')
                self._get_session_from_auth_link(self._auth_link)
            # 更新config
            self._config.set('query', 'session_id', self._session)
            self._config.set('query', 'auth_link', '')
            self._config.save()

        self._headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'weixinchongzhi.scut.edu.cn',
            'Origin': 'https://weixinchongzhi.scut.edu.cn',
            'Referer': 'https://weixinchongzhi.scut.edu.cn/wechat/icinfo/query.html?aid=0030000000011201&name=%E5%AD%A6%E7%94%9F%E7%A9%BA%E8%B0%83%E8%B4%B9',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self._cookies = {'JSESSIONID': self._session}

        self._WAT_FORM_DATA = create_query_form_data(self.auto_query(type=0))
        self._ELE_FORM_DATA = create_query_form_data(self.auto_query(type=1))
        self._AIR_FORM_DATA = create_query_form_data(self.auto_query(type=2))
        logger.debug(f'WAT_FORM_DATA: {self._WAT_FORM_DATA}')
        logger.debug(f'ELE_FORM_DATA: {self._ELE_FORM_DATA}')
        logger.debug(f'AIR_FORM_DATA: {self._AIR_FORM_DATA}')

        self._CSV_FILE_PATH = kwargs.get('csv_file_path', None)

    def _get_session_from_auth_link(self, auth_link):
        """企业微信 > 校园一卡通， 分享的连接"""
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'weixinchongzhi.scut.edu.cn',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        try:
            response = requests.get(auth_link, headers=headers)

            if response.status_code == 200:
                set_cookie = response.headers.get('Set-Cookie')
                if set_cookie:
                    logger.debug(f'set_cookie: {set_cookie}')
                    self._session = set_cookie.split(';')[0].split('=')[1]
                else:
                    logger.debug(f'set_cookie: None')
                    raise Exception("Set-Cookie header not found in the response")
            else:
                response.raise_for_status()  # 如果请求失败，会抛出异常
        except requests.RequestException as e:
            logger.error(f'Error: {e}')

    def refresh_session(self):
        """session失效刷新"""
        pass

    def query_elec_room_info(self, aid, area, building, floor, room):
        """余额查询"""
        url = create_url(api_name='basicQuery/queryElecRoomInfo')
        params = {
            'aid': aid,
            'area': area,
            'building': building,
            'floor': floor,
            'room': room
        }

        try:
            response = requests.post(url, data=params, cookies=self._cookies, headers=self._headers)
            response.raise_for_status()  # 如果请求失败，会抛出异常
            logger.debug(f'queryElecRoomInfo response: {response.json()}')
            # print('Query response:', response.json())
            return response.json()['errmsg']
        except requests.RequestException as e:
            logger.error(f'Error querying room info: {e}')
            # print('Error querying room info:', e)

    def auto_query(self, type: int):
        """
        房间信息查询
        :param type: 0(水)，1(电)，2(空调)
        :return: {'account','building','floor','id','refreshTime','room','schoolId','type'}
        """
        url = create_url(api_name='icinfo/autoQuery')
        params = {
            'type': type
        }

        try:
            response = requests.post(url, data=params, cookies=self._cookies, headers=self._headers)
            response.raise_for_status()
            response_json = response.json()
            logger.debug(f'autoQuery response: {response_json}')
            if response_json == 1:
                # session 过期
                self._config.set('query', 'session_id', '')
                self._config.save()
                logger.critical(f'session expired, refresh your auth link')
            return response_json
        except requests.RequestException as e:
            logger.error('Error autoQuery:', e)

    def query_balance(self):
        """
        查询水电空调余额
        :return: {'timestamp'. 'water_balance', 'electricity_balance', 'air_conditioner_balance'}
        """
        query_response = self.query_elec_room_info(**self._WAT_FORM_DATA), self.query_elec_room_info(
            **self._ELE_FORM_DATA), self.query_elec_room_info(**self._AIR_FORM_DATA)
        record_data = {
            'timestamp': datetime.now().isoformat(),
            'water_balance': query_response[0].replace('剩余水费', '').split(',')[-1],
            'electricity_balance': query_response[1].replace('房间当前剩余电量', ''),
            'air_conditioner_balance': query_response[2].replace('房间当前剩余金额', '')
        }
        return record_data

    def record_data(self):
        """disposed"""
        record_data = self.query_balance()
        recorder = CSVRecordHandler(csv_file_path=self._CSV_FILE_PATH)
        recorder.record(record_data)


if __name__ == '__main__':
    query = ElecRoomQuery(auth_link=None, session_id=None, csv_file_path='test_data.csv')
    query.record_data()
