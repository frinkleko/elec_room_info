from pathlib import Path
from omegaconf import OmegaConf, DictConfig


class Config:
    def __init__(self, conf_file):
        self._conf_path = conf_file
        self._conf: DictConfig = OmegaConf.load(conf_file)

    def __getitem__(self, name):
        return self._conf.__getitem__(name)

    def __getattr__(self, name):
        return self._conf.__getattr__(name)

    def __setitem__(self, name, value):
        self._conf.__setitem__(name, value)

    def __str__(self):
        return OmegaConf.to_yaml(self._conf)

    def save(self, conf_path=None):
        if conf_path is not None:
            OmegaConf.save(self._conf, conf_path)
        else:
            OmegaConf.save(self._conf, self._conf_path)

    def to_yaml(self):
        return OmegaConf.to_yaml(self._conf)

    @classmethod
    def to_dict(cls, cfg: DictConfig):
        return OmegaConf.to_container(cfg, resolve=True)

    @classmethod
    def auto_config(cls, path: Path):
        conf = {}

        conf['general'] = {

        }
        conf['addon'] = {
            'balance_monitor': True,
            'deposit_monitor': True
        }
        conf['query'] = {
            'auth_link': '',
            'session_id': ''
        }
        conf['record_csv'] = {
            'csv_file_path': 'data/records/query_data.csv',
        }
        conf['email'] = {
            'sender_email': 'mail@example.com',
            'sender_name': 'root',
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'smtp_user': 'mail@example.com',
            'smtp_password': '<passwd>'
        }

        conf['balance_monitor'] = {
            'to_emails': 'mail@example.com',
            'threshold': {
                'water_balance': 1,
                'electricity_balance': 3,
                'air_conditioner_balance': 5
            }
        }

        if not path.exists():
            path.touch()
        with path.open('w') as f:
            OmegaConf.save(conf, f)


if __name__ == '__main__':
    CONFIG_PATH = Path(__file__).parents[3] / 'data' / 'configs' / 'config.yaml'
    Config.auto_config(CONFIG_PATH)

    config = Config(CONFIG_PATH)
    print(config)

    # config.addon.balance_monitor = False
    # print(config)
    # config.save()
