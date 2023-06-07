from celery import Celery, signals
from redis import Redis
import os

from django.conf import settings
import logging


@signals.celeryd_init.connect
def celery_init(*args, **kwargs):
	redis_client = Redis(host='127.0.0.1', port=6379)
	redis_client.delete('is_all_telegram_bots_already_started')

@signals.setup_logging.connect
def celery_logging_config(*args, **kwargs):
	celery_logger = logging.getLogger('celery')
	celery_logger.setLevel(logging.INFO)

	celery_logger.handlers = []
	celery_logger.filters = []

	info_file_handler = logging.FileHandler(settings.BASE_DIR / 'logs/celery_info.log')
	info_file_handler.setLevel(logging.INFO)

	error_file_handler = logging.FileHandler(settings.BASE_DIR / 'logs/celery_error.log')
	error_file_handler.setLevel(logging.WARNING)

	celery_logger.addHandler(info_file_handler)
	celery_logger.addHandler(error_file_handler)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'constructor_telegram_bots.settings')

celery_app = Celery('constructor_telegram_bots')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(['telegram_bots'])
