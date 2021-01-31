from abc import ABCMeta, abstractmethod
from utils.base_utils import singleton_func


class BaseClient(metaclass=ABCMeta):

    def __init__(self, db_name, db_host, db_port, db_pass=None, **kwargs):
        self.db_name = db_name
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_port = db_port
        self.db_conn = self.get_connect()

    @abstractmethod
    @singleton_func
    def get_connect(self, **kwargs):
        ...

    @abstractmethod
    def fetch_proxy(self, **kwargs):
        ...

    @abstractmethod
    def remove_proxy(self, **kwargs):
        ...

    @abstractmethod
    def create_proxy(self, **kwargs):
        ...

    def count_proxy(self, **kwargs):
        ...
