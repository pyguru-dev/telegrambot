from celery import shared_task

from django.conf import settings

from .models import User

from requests import Response
import requests

import time


@shared_task
def check_users_first_name():
	for user in User.objects.all():
		response: Response = requests.get(f'https://api.telegram.org/bot{settings.CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN}/getChat?chat_id={user.telegram_id}')

		if response.status_code == 200:
			first_name: str = response.json()['result']['first_name']

			if user.first_name != first_name:
				user.first_name = first_name
				user.save()

		time.sleep(0.1)
