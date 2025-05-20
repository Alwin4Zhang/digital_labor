#!/bin/bash
# 客户端启动
# celery -A mq.tasks  worker --loglevel=info --pool=threads  --concurrency=8

# 消息队列监控
# celery -A mq.tasks flower --loglevel=INFO

# 服务启动
# python api.py