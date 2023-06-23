from celery import Celery, signals
from redis import Redis
import os


@signals.celeryd_init.connect
def celery_init(*args, **kwargs):
	redis_client = Redis(host='127.0.0.1', port=6379)
	redis_client.delete('is_all_telegram_bots_already_started')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'constructor_telegram_bots.settings')

celery_app = Celery('constructor_telegram_bots')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(['telegram_bots'])
