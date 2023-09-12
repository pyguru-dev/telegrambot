from django.conf import settings

from typing import Optional
import requests


def check_telegram_bot_api_token(api_token: str) -> Optional[str]:
	if settings.TEST:
		return f'{api_token}_test_telegram_bot'

	responce: requests.Response = requests.get(f'https://api.telegram.org/bot{api_token}/getMe')

	if responce.status_code == 200:
		return responce.json()['result']['username']
