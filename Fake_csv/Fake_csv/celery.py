import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Fake_csv.settings')

app = Celery('Fake_csv', backend='redis')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()