from django.conf import settings
import requests


def create_user(user) -> None:
	if not settings.TEST:
		print({'username': f'_{user.id}', 'password': user.auth_token.key})
		requests.post('http://127.0.0.1:99/users/', json={'username': f'_{user.id}', 'password': user.auth_token.key})

def delete_user(user) -> None:
	if not settings.TEST:
		requests.delete(f'http://127.0.0.1:99/users/_{user.id}/')

def add_plugin(plugin) -> None:
	if not settings.TEST:
		requests.post(
			'http://127.0.0.1:99/scripts/',
			json={
				'username': f'_{plugin.user.id}',
				'telegram_bot': plugin.telegram_bot.id,
				'plugin_id': plugin.id,
				'name': plugin.name,
				'text': plugin.code,
			}
		)

def update_plugin(plugin) -> None:
	if not settings.TEST:
		requests.post(
			'http://127.0.0.1:99/scripts/',
			json={
				'username': f'_{plugin.user.id}',
				'telegram_bot': plugin.telegram_bot.id,
				'plugin_id': plugin.id,
				'name': plugin.name,
				'text': plugin.code,
			}
		)

def delete_plugin(plugin) -> None:
	if not settings.TEST:
		requests.delete(
			'http://127.0.0.1:99/scripts/',
			json={
				'username': f'_{plugin.user.id}',
				'telegram_bot': plugin.telegram_bot.id,
				'name': plugin.name,
			}
		)

def replace_text_variables(telegram_bot, text: str, text_variables: dict) -> str:
	if settings.TEST:
		return text

	return requests.post(
		'http://127.0.0.1:99/generate/template/',
		headers={},
		json={
			'username': f'_{telegram_bot.owner.id}',
			'telegram_bot': telegram_bot.id,
			'template': text,
			'token': telegram_bot.owner.auth_token.key,
			'context': text_variables,
		}
	).json()['response']
