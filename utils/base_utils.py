import os
import time
import datetime
import threading


class IdCounter(object):
    _lock = threading.RLock()

    def __init__(self, initial_value=0):
        self._value = initial_value

    def incr(self, delta=1):
        '''
        Increment the counter with locking
        '''
        with IdCounter._lock:
            self._value += delta
            return self._value


id_counter = IdCounter()


def generate_unique_id():
    return '{}{}'.format(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"), str(id_counter.incr()))


def singleton_cls(cls, *args, **kwargs):
    instances = {}
    def _singleton():
        key = str(cls) + str(os.getpid())
        if key not in instances:
            instances[key] = cls(*args, **kwargs)
        return instances[key]
    return _singleton


def singleton_func(func):
    instance = {}
    def _singleton(*args, **kwargs):
        key = str(func) + str(os.getpid())
        if key not in instance:
            instance[key] = func(*args, **kwargs)
        return instance[key]
    return _singleton



def current_timestamp():
    return int(time.time() * 1000)