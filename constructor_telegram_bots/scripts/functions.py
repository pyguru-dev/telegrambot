from typing import Union
import requests
import random
import json


def generator_random_string(length: int, chars: str) -> str:
	random_string = ''
	for num in range(length):
		random_string += random.choice(chars)
	return random_string

def check_telegram_bot_api_token(api_token: str) -> Union[str, None]:
	responce = requests.get(url=f'https://api.telegram.org/bot{api_token}/getMe')
	if responce.status_code == 200:
		responce_json: dict = json.loads(responce.text)
		return responce_json['result']['username']
	else:
		return None
