from django.conf.global_settings import TIME_ZONE

BROKER_URL = 'amqp://celery:celery@localhost:5672/dev'
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = 'amqp'
# thats where celery will store scheduled tasks in case you restart the broker:
CELERYD_STATE_DB = "/"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
