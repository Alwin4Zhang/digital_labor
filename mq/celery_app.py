import os
import time
from datetime import datetime

from celery import Celery

celery_app = Celery("tasks",
             broker=os.environ.get('CELERY_BROKER_URL', 'redis://'),
             backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis'))

celery_app.conf.update(
    task_serializer="pickle",
    result_serializer='pickle',
    accept_content=['pickle','json'],
    timezone='Asia/Shanghai',
    enable_utc = True,
    broker_pool_limit=None,
    # worker_prefetch_multiplier=8,
    # task_acks_late=True
    worker_redirect_stdouts=False,
    worker_hijack_root_logger=False,
    worker_max_task_per_child=100
)

# celery_app.conf.accept_content = ['pickle', 'json', 'msgpack', 'yaml']
celery_app.conf.worker_send_task_events = True


if __name__ == "__main__":
    celery_app.start()