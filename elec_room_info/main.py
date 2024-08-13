from utils.query import ElecRoomQuery
from utils.config import Config
from addon import BalanceMonitor


import argparse
import threading
import time


QUERY_INTERVAL = 30  # 30 * 60  # 30分钟，以秒为单位
RECORD = True


def start_periodic_queries(conf: Config):
    query = ElecRoomQuery(config=conf)
    monitor = BalanceMonitor(config=conf) if conf['addon']['balance_monitor'] else None
    while True:
        query.record_data()
        if monitor is not None:
            monitor.check()
            monitor.deposit()
        time.sleep(eval(conf.get('record_csv', 'query_interval', fallback=QUERY_INTERVAL)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file', default="data/configs/config.ini")
    args = parser.parse_args()

    config = Config()
    config.read(args.config)

    if RECORD:
        thread = threading.Thread(target=start_periodic_queries, args=[config,])  # , daemon=True
        thread.start()
