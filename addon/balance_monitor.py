"""余额监控插件"""
from utils.record_csv import CSVRecordHandler
from utils.mail import EmailSender

from utils.log import get_logger
logger = get_logger(__name__)


class BalanceMonitor:
    def __init__(self, **kwargs):
        self._config = kwargs.get('config')

        self.csv_file_path = self._config['record_csv']['csv_file_path']
        self.csv_handler = CSVRecordHandler(self.csv_file_path)
        self.threshold = eval(self._config['balance_monitor']['threshold'])
        self.email_sender = EmailSender(config=self._config)
        self.to_emails = self._config['balance_monitor']['to_emails']

    def check(self):
        last_record = self.csv_handler.get_latest()
        logger.debug('last_record: %s', last_record)

        if last_record['water_balance'] < self.threshold['water_balance'] or \
                last_record['electricity_balance'] < self.threshold['electricity_balance'] or \
                last_record['air_conditioner_balance'] < self.threshold['air_conditioner_balance']:
            logger.info(f'余额不足: {last_record}')
            if self.email_sender:
                subject = 'Dorm Electricity Balance Warning'
                message = (f"余额不足：\n 水费余额：{last_record['water_balance']}\n 电费余额：{last_record['electricity_balance']}\n "
                           f"空调余额：{last_record['air_conditioner_balance']}")
                self.email_sender.send_email(self.to_emails, subject=subject, message=message)

    def deposit(self):
        # 充值检测
        last_record = self.csv_handler.get_latest()
        last_second_record = self.csv_handler.get(-2)

        message = ''

        if last_record['water_balance'] > last_second_record['water_balance']:
            message += f"水费充值{last_record['water_balance'] - last_second_record['water_balance']}元\n"
        if last_record['electricity_balance'] > last_second_record['electricity_balance']:
            message += f"电费充值{last_record['electricity_balance'] - last_second_record['electricity_balance']}元\n"
        if last_record['air_conditioner_balance'] > last_second_record['air_conditioner_balance']:
            message += (f"空调充值{last_record['air_conditioner_balance'] - last_second_record['air_conditioner_balance']}"
                        f"元\n")

        if message != '':
            logger.info(f'检测到充值: {last_record}')
            subject = 'Dorm Deposit Sniffer'
            self.email_sender.send_email(self.to_emails, subject=subject, message=message)


if __name__ == '__main__':
    from utils.config import Config
    import os
    os.chdir('..')
    test_config = Config()
    test_config.read('test_config.ini', encoding='utf-8')
    monitor = BalanceMonitor(config=test_config)
    monitor.check()
    monitor.deposit()
