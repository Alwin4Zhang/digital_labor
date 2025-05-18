# -*- encoding: utf-8 -*-
'''
@File    :   service_trace.py
@Time    :   2022/09/24 10:22:39
@Author  :   韦国迎 
'''

import logging
from logging import Filter
from contextvars import ContextVar

# 线程变量key
request_id = "request_id"
# 线程变量：链路追踪容器
request_id_context = ContextVar(request_id, default=None)


class TraceIDFilter(Filter, object):
    def __init__(self, name):
        logging.Filter.__init__(self)
        self.name = name

    def filter(self, record):
        record.traceId = request_id_context.get()
        return True