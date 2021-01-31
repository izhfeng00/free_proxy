import re

class Proxy:
    """
    proxy schema
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __str__(self):
        return f'{self.host}:{self.port}'

    def __repr__(self):
        return self.__str__()

    def to_string(self):
        return self.__str__()

    @classmethod
    def check_proxy(cls, proxy: str):
        ipv4_pattern = '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}:((6553[0-5])' \
                       '|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))$'
        if re.match(ipv4_pattern, proxy) is None:
            return False
        return True

    @classmethod
    def to_proxy(cls, proxy):
        if isinstance(proxy, bytes):
            proxy = str(proxy, 'utf-8')
        elif isinstance(proxy, str):
            pass
        else:
            raise TypeError(f"proxy must be bytes or str, not {proxy.__class__.__name__}")
        if cls.check_proxy(proxy):
            return Proxy(host=proxy.split(':')[0], port=proxy.split(':')[1])
        return None
