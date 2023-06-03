from celery import Celery
import os

from celery.signals import setup_logging
from django.conf import settings
import logging


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'constructor_telegram_bots.settings')

celery_app = Celery('constructor_telegram_bots')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(['telegram_bots'])

@setup_logging.connect
def celery_logging(*args, **kwargs):
	celery_logger = logging.getLogger('celery')
	celery_logger.setLevel(logging.NOTSET)

	celery_logger.handlers = []
	celery_logger.filters = []

	info_file_handler = logging.FileHandler(settings.BASE_DIR / 'logs/celery_info.log')
	info_file_handler.setLevel(logging.INFO)

	error_file_handler = logging.FileHandler(settings.BASE_DIR / 'logs/celery_error.log')
	error_file_handler.setLevel(logging.WARNING)

	celery_logger.addHandler(info_file_handler)
	celery_logger.addHandler(error_file_handler)
