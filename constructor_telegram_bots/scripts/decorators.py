from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import render

import json

def get_user_data(func):
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]

		kwargs.update(
			{
				'data': {
					'page': {
						'url': request.path,
					},
					'user': {
						'is_authenticated': request.user.is_authenticated,
					},
				},
			}
		)

		if request.user.is_authenticated:
			kwargs['data']['user'].update(
				{
					'username': request.user.username
				}
			)

		return func(*args, **kwargs)
	return wrapper

def is_auth(render_page: bool):
	def decorator(func):
		def wrapper(*args, **kwargs):
			request: WSGIRequest = args[0]

			if request.user.is_authenticated:
				return func(*args, **kwargs)
			else:
				if render_page:
					data =	{
						'title': 'Страница не найдена',
						'meta': {
							'url': '/',
						},
						'content': {
							'heading': 'Ошибка 404!',
							'text': 'Страница не найдена, автоматический переход на главную страницу через 3 секунды.',
						},
					}

					return render(request, '.html', context=data)
				else:
					return HttpResponseBadRequest('Сначала авторизуйтесь на сайте!')
		return wrapper
	return decorator

def check_request_data_items(needs_items: tuple):
	def decorator(func):
		def wrapper(*args, **kwargs):
			request: WSGIRequest = args[0]
			if request.method == 'POST':
				data = json.loads(request.body)

				data_items = []
				for data_item in tuple(data.keys()):
					data_items.append(data_item)

				if tuple(data_items) == needs_items:
					for data_item in tuple(data.keys()):
						if data_item in data_items:
							kwargs.update(
							{
								data_item: data[data_item],
							}
						)

					return func(*args, **kwargs)
				else:
					return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
			else:
				return HttpResponseBadRequest('Неправильный метод запроса!')
		return wrapper
	return decorator

def check_telegram_bot_id(render_page: bool):
	def decorator(func):
		def wrapper(*args, **kwargs,):
			if 'telegram_bot_id' in kwargs:
				request: WSGIRequest = args[0]
				telegram_bot_id = kwargs['telegram_bot_id']

				if request.user.telegram_bots.filter(id=telegram_bot_id).exists():
					del kwargs['telegram_bot_id']
					kwargs.update(
						{
							'telegram_bot': request.user.telegram_bots.get(id=telegram_bot_id)
						}
					)

					return func(*args, **kwargs)
				else:
					if render_page:
						data =	{
							'title': 'Страница не найдена',
							'meta': {
								'url': '/personal_cabinet/',
							},
							'content': {
								'heading': 'Ошибка 404!',
								'text': 'Страница не найдена, автоматический переход в личный кабинет через 3 секунды.'
							},
						}

						return render(request, '.html', context=data)
					else:
						return HttpResponseBadRequest('Telegram бот не найден!')
			else:
				raise ValueError('The argument telegram_bot_id is missing!')
		return wrapper
	return decorator