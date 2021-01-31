import settings
from abc import ABCMeta, abstractmethod
from importlib import import_module
from utils.base_utils import singleton_func


class BaseConfig(metaclass=ABCMeta):

    def __init__(self):
        self.check_config()

    @abstractmethod
    def check_config(self):
        ...

    @singleton_func
    @abstractmethod
    def db(self):
        ...

    def server_info(self):
        ...

    def detector_info(self):
        ...


class Config(BaseConfig):

    def __init__(self):
        super(Config, self).__init__()

    def check_config(self):
        if not ((0 < settings.RES_RATIO) and (settings.RES_RATIO < 1)):
            raise ValueError(f'RES_RATIO should between 0 and 1. Current RES_RATIO is set as {settings.RES_RATIO}.')
        if not settings.FAIL_PUNISH < 0:
            raise ValueError('FAIL_PUNISH should less then 0.')

    @singleton_func
    def db(self):
        return import_module(f'db.{settings.DB_CLIENT.lower()}_client').DBClient(
            db_host = settings.DB_HOST,
            db_port = settings.DB_PORT,
            db_name = settings.DB_NAME,
            db_pass = settings.DB_PASS
        )

    def server_info(self):
        return {
            'host': settings.SERVER_HOST,
            'port': settings.SERVER_PORT,
        }

    def detector_info(self):
        return {
            'interval': settings.DETECTOR_INTERVAL,
            'f_s_ratio': settings.F_S_RATIO,
        }

    def fetch_info(self):
        return {
            'success_award': settings.SUCCESS_AWARD,
            'fail_punish': settings.FAIL_PUNISH,
            'res_ratio': settings.RES_RATIO,
            'fetch_limit': settings.FETCH_LIMIT
        }


config = Config()
