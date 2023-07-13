import requests


def create_user(user) -> None:
	requests.post('http://127.0.0.1:99/users/', json={'username': f'_{user.id}', 'password': user.auth_token.key})

def delete_user(user) -> None:
	requests.delete(f'http://127.0.0.1:99/users/{user.username}/')

def add_plugin(plugin) -> None:
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
	requests.delete(
		'http://127.0.0.1:99/scripts/',
		json={
			'username': f'_{plugin.user.id}',
			'telegram_bot': plugin.telegram_bot.id,
			'name': plugin.name,
		}
	)

def replace_text_variables(telegram_bot, text: str, text_variables: dict) -> str:
	return requests.post(
		'http://127.0.0.1:99/generate/template/',
		json={
			'username': f'_{telegram_bot.owner.id}',
			'telegram_bot': telegram_bot.id,
			'token': telegram_bot.owner.auth_token.key,
			'template': text,
			'context': text_variables,
		}
	).json()['response']
