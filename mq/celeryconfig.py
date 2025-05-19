# broker_url = 'pyamqp://'
# result_backend = 'rpc://'

broker_url = 'redis://localhost:6379/0'
celery_result_backend = 'redis://localhost:6379/0'
task_send_sent_event = False

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = True