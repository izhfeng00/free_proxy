import random
from redis import Redis
from entity.proxy import Proxy
from db.base_client import BaseClient
from entity.runtime_config import config
from utils.base_utils import generate_unique_id, current_timestamp


class DBClient(BaseClient):

    def __init__(self, db_name, db_host, db_port, db_pass=None, **kwargs):
        super(DBClient, self).__init__(db_name, db_host, db_port, db_pass, **kwargs)

    def get_connect(self, **kwargs):
        return Redis(host=self.db_host, port=self.db_port,
                     db=self.db_name, password=self.db_pass,
                     **kwargs)

    def fetch_proxy(self, key) -> [Proxy]:
        """

        :return: array of proxies, count 10
        """
        proxies = []
        union_id = f'fetch_{generate_unique_id()}'
        try:
            fetch_info = config.fetch_info()
            result_length = self.db_conn.zunionstore(union_id, {f'{key}_success': fetch_info.get('success_award', 8),
                                                                f'{key}_fail': fetch_info.get('fail_punish', 2)})
            if result_length:
                union_result = self.db_conn.zrevrange(union_id, 0, -1, withscores=True)
                fetch_count = fetch_info.get('fetch_limit', 10) if result_length > fetch_info.get('fetch_limit', 10) else result_length
                top_sample_result_count = round(fetch_count*fetch_info.get('res_ratio', 0.8))
                proxies.extend(random.sample(union_result[:top_sample_result_count], top_sample_result_count))
                if top_sample_result_count < fetch_count:
                    proxies.extend(random.sample(union_result[top_sample_result_count:],
                                                 fetch_count-top_sample_result_count))
                proxies = [tp[0] for tp in sorted(proxies, key=lambda x: x[1], reverse=True)]
        except Exception:
            # TODO log
            raise
            return []
        else:
            return [Proxy.to_proxy(proxy) for proxy in proxies]
        finally:
            self.db_conn.delete(union_id)

    def remove_proxy(self, key, member):
        self.create_proxy(f'{key}_removed', member, current_timestamp())

    def create_proxy(self, key, member, value=None):
        if isinstance(member, str):
            member = [member]
        for proxy in member:
            if Proxy.check_proxy(proxy):
                # TODO log success
                pass
            else:
                # TODO log fail
                member.remove(proxy)
        if member:
            self._create(key, member, value)

    def count_proxy(self, key, postfix='success'):
        return self._count(f'{key}_{postfix}')

    def modify_score(self, key, member, amount):
        postfix = 'failed' if amount < 0 else 'success'
        self._modify(key=f'{key}_{postfix}', member=member, amount=amount)

    def _create(self, key, member, value=None, nx=True):
        if isinstance(member, str):
            member = [member]
        self.db_conn.zadd(key, dict(zip(member, [0 if value is None else value]*len(member))), nx=nx)

    def _exists(self, key, member):
        if self.db_conn.zscore(name=key, value=member) is None:
            return False
        return True

    def _count(self, key):
        return self.db_conn.zcard(name=key)

    def _modify(self, key, member, amount):
        self.db_conn.zincrby(name=key, amount=amount, value=member)

    def _remove(self, key, member):
        if isinstance(member, str):
            member = [member]
        self.db_conn.zrem(name=key, values=member)
