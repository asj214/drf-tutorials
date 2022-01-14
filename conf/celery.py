import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('tasks',
    broker='amqp://{0}:{1}@{2}:{3}/vhost'.format(
        settings.RABBIT_MQ.get('username'),
        settings.RABBIT_MQ.get('password'),
        settings.RABBIT_MQ.get('host'),
        settings.RABBIT_MQ.get('port'),
    ),
    backend='rpc://',
    include=['conf.tasks'])

# app.autodiscover_tasks()
# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)