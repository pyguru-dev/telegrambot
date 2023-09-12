from django.conf import settings

from asgiref.sync import sync_to_async
import requests
import jinja2


def create_user(user) -> None:
	if settings.DEBUG or settings.TEST:
		return

	requests.post('http://127.0.0.1:99/users/', json={'user_id': user.id, 'token': user.auth_token.key})

def delete_user(user) -> None:
	if settings.DEBUG or settings.TEST:
		return

	requests.delete(f'http://127.0.0.1:99/users/{user.id}/')

def add_plugin(plugin) -> None:
	if settings.DEBUG or settings.TEST:
		return

	requests.post('http://127.0.0.1:99/plugins/', json={
		'user_id': plugin.user.id,
		'token': plugin.user.auth_token.key,
		'telegram_bot_id': plugin.telegram_bot.id,
		'plugin_id': plugin.id,
		'name': plugin.name,
		'code': plugin.code,
	})

def update_plugin(plugin) -> None:
	if settings.DEBUG or settings.TEST:
		return

	requests.post('http://127.0.0.1:99/plugins/', json={
		'user_id': plugin.user.id,
		'token': plugin.user.auth_token.key,
		'telegram_bot_id': plugin.telegram_bot.id,
		'plugin_id': plugin.id,
		'name': plugin.name,
		'code': plugin.code,
	})

def delete_plugin(plugin) -> None:
	if settings.DEBUG or settings.TEST:
		return

	requests.delete('http://127.0.0.1:99/plugins/', json={
		'user_id': plugin.user.id,
		'telegram_bot_id': plugin.telegram_bot.id,
		'name': plugin.name,
	})

def replace_text_variables(telegram_bot, text: str, text_variables: dict) -> str:
	if settings.DEBUG or settings.TEST:
		environment = jinja2.Environment()
		template: jinja2.Template = environment.from_string(text)
		return template.render(text_variables)

	return requests.post('http://127.0.0.1:99/generate/template/', json={
		'user_id': telegram_bot.owner.id,
		'token': telegram_bot.owner.auth_token.key,
		'telegram_bot_id': telegram_bot.id,
		'text': text,
		'text_variables': text_variables,
	}).json()['response']

async def areplace_text_variables(telegram_bot, text: str, text_variables: dict) -> str:
	return await sync_to_async(replace_text_variables)(telegram_bot=telegram_bot, text=text, text_variables=text_variables)
