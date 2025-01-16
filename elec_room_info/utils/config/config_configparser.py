import configparser
import pathlib

CONFIG_PATH = pathlib.Path('data/configs/config.ini')


class Config(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        self.config_path = ''

    def auto_config(self):
        self['general'] = {

        }
        self['addon'] = {
            'balance_monitor': 'True',
        }
        self['query'] = {
            'auth_link': '',
            'session_id': ''
        }
        self['record_csv'] = {
            'csv_file_path': 'query_data.csv',
            'query_interval': 30 * 60
        }
        self['email'] = {
            'SENDER_EMAIL': 'mail@example.com',
            'SENDER_NAME': 'root',
            'SMTP_SERVER': 'smtp.example.com',
            'SMTP_PORT': 587,
            'SMTP_USER': 'mail@example.com',
            'SMTP_PASSWORD': '<passwd>'
        }

        self['balance_monitor'] = {
            'to_emails': 'mail@example.com',
            'threshold': {
                'water_balance': 1,
                'electricity_balance': 3,
                'air_conditioner_balance': 5
            }
        }

        if not CONFIG_PATH.exists():
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
