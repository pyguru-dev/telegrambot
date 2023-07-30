from django.conf import settings

import requests


def create_user(user) -> None:
	if not settings.TEST:
		requests.post('http://127.0.0.1:99/users/', {'user_id': user.id, 'token': user.auth_token.key})

def delete_user(user) -> None:
	if not settings.TEST:
		requests.delete(f'http://127.0.0.1:99/users/{user.id}/')

def add_plugin(plugin) -> None:
	if not settings.TEST:
		requests.post('http://127.0.0.1:99/plugins/', {
			'user_id': plugin.user.id,
			'token': plugin.user.auth_token.key,
			'telegram_bot_id': plugin.telegram_bot.id,
			'plugin_id': plugin.id,
			'name': plugin.name,
			'code': plugin.code,
		})

def update_plugin(plugin) -> None:
	if not settings.TEST:
		requests.post('http://127.0.0.1:99/plugins/', {
			'user_id': plugin.user.id,
			'token': plugin.user.auth_token.key,
			'telegram_bot_id': plugin.telegram_bot.id,
			'plugin_id': plugin.id,
			'name': plugin.name,
			'code': plugin.code,
		})

def delete_plugin(plugin) -> None:
	if not settings.TEST:
		requests.delete('http://127.0.0.1:99/plugins/', {
			'user_id': plugin.user.id,
			'telegram_bot_id': plugin.telegram_bot.id,
			'name': plugin.name,
		})

def replace_text_variables(telegram_bot, text: str, text_variables: dict) -> str:
	if settings.TEST:
		return text

	return requests.post('http://127.0.0.1:99/generate/template/', {
		'user_id': telegram_bot.owner.id,
		'token': telegram_bot.owner.auth_token.key,
		'telegram_bot_id': telegram_bot.id,
		'text': text,
		'text_variables': text_variables,
	}).json()['response']
