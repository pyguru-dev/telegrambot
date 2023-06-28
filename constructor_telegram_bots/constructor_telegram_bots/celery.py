from celery import Celery, signals

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'constructor_telegram_bots.settings')


celery_app = Celery('constructor_telegram_bots')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(['telegram_bots'])


@signals.celeryd_after_setup.connect
def celery_after_setup(*args, **kwargs):
	from telegram_bots.tasks import start_all_telegram_bots
	start_all_telegram_bots.delay()
