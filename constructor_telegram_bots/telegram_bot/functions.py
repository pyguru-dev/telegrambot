from typing import Union
import requests
import json


def check_telegram_bot_api_token(api_token: str) -> Union[str, None]:
	responce = requests.get(url=f'https://api.telegram.org/bot{api_token}/getMe')
	if responce.status_code == 200:
		responce_json = json.loads(responce.text)
		return responce_json['result']['username']
	else:
		return None
