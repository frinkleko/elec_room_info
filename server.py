# server.py

from flask import Flask
import requests
import threading
import time
import random
from datetime import datetime
from utils.record_csv import init_csv, record_to_csv

from utils import log

logger = log.getLogger(__name__)

app = Flask(__name__)

# 配置
COOKIE_NAME = 'JSESSIONID'


# 表单数据
WAT_FORM_DATA = {
    'aid': '0030000000004901',
    'area': '{"area":"","areaname":""}',
    'building': '{"building":"D5f","buildingid":"001001001"}',
    'floor': '{"floor":"7","floorid":"001001001007"}',
    'room': '{"room":"706","roomid":"001001001007006"}'
}

ELE_FORM_DATA = {
    'aid': '0030000000011101',
    'area': '{"area":"","areaname":""}',
    'building': '{"building":"D5f","buildingid":"17"}',
    'floor': '{"floor":"07","floorid":"07"}',
    'room': '{"room":"D5f706","roomid":"D5f706"}'
}

AIR_FORM_DATA = {
    'aid': '0030000000011201',
    'area': '{"area":"","areaname":""}',
    'building': '{"building":"D5f","buildingid":"440113D0135"}',
    'floor': '{"floor":"07","floorid":"440113D013507"}',
    'room': '{"room":"706","roomid":"D5f706"}'
}


QUERY_INTERVAL = 20 * 60  # 20分钟，以秒为单位


# 模拟获取JSESSIONID
def get_session_id():
    # 这里应该从实际的存储或用户请求中获取JSESSIONID
    # 示例中直接返回一个示例值
    return 'D5B370F425A73EC707EB40C874E35A60'


# 创建查询请求的URL
def create_url(path, v):
    return f'https://weixinchongzhi.scut.edu.cn/wechat{path}?v={v}'


# 发送查询请求
def query_elec_room_info(aid, area, building, floor, room):
    v = random.randint(1, 100)  # 生成1到100的随机整数
    url = create_url('/basicQuery/queryElecRoomInfo.html', v)
    params = {
        'aid': aid,
        'area': area,
        'building': building,
        'floor': floor,
        'room': room
    }
    cookies = {COOKIE_NAME: get_session_id()}

    headers = {
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

    try:
        response = requests.post(url, data=params, cookies=cookies, headers=headers)
        response.raise_for_status()  # 如果请求失败，会抛出异常
        print('Query response:', response.json())
        return response.json()['errmsg']
    except requests.RequestException as e:
        print('Error querying room info:', e)


# 定时任务，每20分钟发送一次查询请求
def start_periodic_queries():
    while True:
        query_response = query_elec_room_info(**WAT_FORM_DATA), query_elec_room_info(**ELE_FORM_DATA), query_elec_room_info(**AIR_FORM_DATA)
        record_data = {
            'timestamp': datetime.now().isoformat(),
            'water_balance': query_response[0].replace('剩余水费', '').split(',')[-1],
            'electricity_balance': query_response[1].replace('房间当前剩余电量', ''),
            'air_conditioner_balance': query_response[2].replace('房间当前剩余金额', '')
        }
        record_to_csv(record_data)
        time.sleep(QUERY_INTERVAL)


@app.route('/')
def index():
    query_response = (query_elec_room_info(**WAT_FORM_DATA), query_elec_room_info(**ELE_FORM_DATA), query_elec_room_info(
        **AIR_FORM_DATA))

    return query_elec_room_info(**AIR_FORM_DATA)
    # return 'Server is running. Check the logs for query results.'


if __name__ == '__main__':
    init_csv()
    # 启动定时任务的线程
    thread = threading.Thread(target=start_periodic_queries, daemon=True)
    thread.start()

    # 启动Flask应用
    app.run(port=5000)
