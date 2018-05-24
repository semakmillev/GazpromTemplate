from __future__ import absolute_import
from celery import Celery

app = Celery('tasks',
             backend='amqp://celery:Argo3151@localhost:5672/',
             broker='amqp://celery:Argo3151@localhost:5672/',
             include='queue.tasks')

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json'
)

app.conf.update(
    task_routes = {
        'generate_picture': {'queue': 'TEMPLATE.Q'},
        'tasks.add': {'queue': 'hipri'},
    },
)

