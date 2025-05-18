# -*- encoding: utf-8 -*-
'''
@File    :   singleton.py
@Time    :   2022/09/24 15:05:48
@Author  :   韦国迎 
'''
import threading

# 单例模式
class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance
