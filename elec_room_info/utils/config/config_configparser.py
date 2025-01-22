import configparser
from pathlib import Path

CONFIG_PATH = Path(__file__).parents[3] / 'data' / 'configs' / 'config.ini'


class Config(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        self.config_path = ''

    def auto_config(self):
        self['general'] = {

        }
        self['addon'] = {
            'balance_monitor': 'True',
            'deposit_monitor': 'True'
        }
        self['query'] = {
            'cookies': {
                'TGC': '',
                'UserId': ''
            },
            "bearer_token": '',
            'auth_link': '',
            'session_id': ''
        }
        self['record_csv'] = {
            'csv_file_path': '../data/records/query_data.csv',
            'query_interval': 20 * 60
        }
        self['email'] = {
            'enable': 'False',
            'sender_email': 'mail@example.com',
            'sender_name': 'root',
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'smtp_user': 'mail@example.com',
            'smtp_password': '<passwd>',
            'max_attempts': '3'
        }

        self['pushplus'] = {
            'enable': 'False',
            'token': '<token>',
            'topic': '',
            'channel': 'wechat',
            'max_attempts': '3'
        }

        self['balance_monitor'] = {
            'to_emails': 'mail@example.com',
            'threshold': {
                'water_balance': 5,
                'electricity_balance': 5,
                'air_conditioner_balance': 8
            }
        }

        if not CONFIG_PATH.exists():
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.touch()
        with CONFIG_PATH.open('w') as configfile:
            self.write(configfile)

    def load(self, *args, **kwargs):
        self.config_path = args[0]
        super().read(*args, **kwargs)

    def save(self, config_path=None):
        if config_path is not None:
            self.config_path = config_path
        with open(self.config_path, 'w') as configfile:
            self.write(configfile)


if __name__ == '__main__':
    # Config().auto_config()
    config = Config()
    config.auto_config()
    # config.read('config.ini')
    # if eval(config['addon']['balance_monitor']):
    #     print('eval true')
    # config.save('config.ini')
