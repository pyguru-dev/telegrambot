from celery import shared_task

from telegram_bots.functions import start_all_telegram_bots as _start_all_telegram_bots


@shared_task(once=True)
def start_all_telegram_bots():
	_start_all_telegram_bots()