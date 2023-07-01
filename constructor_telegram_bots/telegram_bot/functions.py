from django.conf import settings

from typing import Union
import requests


def check_telegram_bot_api_token(api_token: str) -> Union[str, None]:
	if settings.TEST:
		return f'{api_token}_test_telegram_bot'

	responce: requests.Response = requests.get(url=f'https://api.telegram.org/bot{api_token}/getMe')

	if responce.status_code == 200:
		return responce.json()['result']['username']

	return None
