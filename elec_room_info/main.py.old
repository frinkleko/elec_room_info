import argparse
import threading
import time

from utils.query import ElecRoomQuery
from utils.config import Config
from omegaconf import DictConfig, OmegaConf
from addon import BalanceMonitor

from elec_room_info.utils.log import get_logger
logger = get_logger(__name__)

# QUERY_INTERVAL = 120  # 2 * 60  # 2分钟，以秒为单位
# RECORD = True


class ElecRoomInfo:
    def __init__(self, conf: Config):
        self._cfg = conf
        self._query = ElecRoomQuery(config=self._cfg)
        self._monitor = BalanceMonitor(config=self._cfg)
        self._query_interval = self._cfg['record_csv']['query_interval']

    def run(self):
        while True:
            self._query.record_data()
            self._monitor.once()
            logger.info(f"休眠 {self._query_interval} 秒，下次查询时间："
                        f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + self._query_interval))}")
            time.sleep(self._query_interval)


def start_periodic_queries(conf: DictConfig):
    query = ElecRoomQuery(config=conf)
    monitor = BalanceMonitor(config=conf) if conf['addon']['balance_monitor'] else None
    while True:
        query.record_data()
        if monitor is not None:
            monitor.check()
            monitor.deposit()
        time.sleep(conf.record_csv.query_interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file', default="../data/configs/config.yaml")
    args = parser.parse_args()

    # config = Config()
    # config.load(args.config)

    config = Config(args.config)

    # if RECORD:
    #     thread = threading.Thread(target=start_periodic_queries, args=[config,])  # , daemon=True
    #     thread.start()

    ElecRoomInfo(config).run()
