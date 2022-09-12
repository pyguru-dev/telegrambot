from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from constructor.models import TelegramBotModel, TelegramBotCommandModel
import json

def get_navbar_data(func): # Функция для получения данных для NavBar'а 
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]

		if Group.objects.filter(name='free_accounts').exists() == False:
			free_accounts_group = Group.objects.create(name='free_accounts')
			free_accounts_group.save()
		if Group.objects.filter(name='paid_accounts').exists() == False:
			paid_accounts_group = Group.objects.create(name='paid_accounts')
			paid_accounts_group.save()

		if request.user.is_authenticated:
			data = {
				'buttons': {
					'button_1': {
						'id': 'profileButtonLink',
						'onclick': f"window.location.href = '/account/view/{request.user.username}/';",
						'text': 'Профиль',
					},
					'button_2': {
						'id': 'signOutButtonLink',
						'onclick': f"signOut('{request.user.username}');",
						'text': 'Выйти',
					},
					'button_3': {
						'id': 'constructorButtonLink',
						'onclick': f"window.location.href = '/constructor/{request.user.username}/';",
						'text': 'Конструктор',
					},
				},
			}
		else:
			data = {
				'buttons': {
					'button_1': {
						'id': 'authorizationButtonLink',
						'onclick': "window.location.href = '/authorization/';",
						'text': 'Авторизация',
					},
					'button_2': {
						'id': 'registrationButtonLink',
						'onclick': "window.location.href = '/registration/';",
						'text': 'Регистарция',
					},
				},
			}

		kwargs.update(
			{
				'data': data,
			}
		)

		return func(*args, **kwargs)
	wrapper.__name__ = func.__name__
	return wrapper

def if_user_authed(func): # Декоратор для проверки авторизован ли пользователь
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]
		if request.user.is_authenticated:
			login, username = request.user.username, kwargs['username']
			if login == username:
				return func(*args, **kwargs)
			else:
				return HttpResponseBadRequest(f'Ваш Login "{login}", а не "{username}"')
		else:
			return redirect('/authorization/')
	wrapper.__name__ = func.__name__
	return wrapper

def if_user_not_authed(func): # Декоратор для проверки не авторизован ли пользователь
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]
		if request.user.is_authenticated == False:
			return func(*args, **kwargs)
		else:
			return redirect('/')
	wrapper.__name__ = func.__name__
	return wrapper

def check_request_data_items(needs_items: dict): # Декоратор для проверки значений в request запросе
	def decorator(func):
		def wrapper(*args, **kwargs):
			request: WSGIRequest = args[0]
			if request.method == 'POST':
				data = json.loads(request.body)

				data_items = []
				for data_item in tuple(data.items()):
					data_items.append(data_item[0])

				if data_items == needs_items:
					kwargs.update(
						{
							'data': data,
						}
					)

					return func(*args, **kwargs)
				else:
					return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
			else:
				return HttpResponseBadRequest('Неправильный метод запроса!')
		wrapper.__name__ = func.__name__
		return wrapper
	return decorator

def check_max_bots_count_for_account(func):
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]

		if TelegramBotModel.objects.filter(owner_id=request.user.id).count() >= 1 and request.user.groups.filter(name='free_accounts').exists():
			return HttpResponseBadRequest('У вас уже максимальное количество ботов!')
		elif TelegramBotModel.objects.filter(owner_id=request.user.id).count() >= 5 and request.user.groups.filter(name='paid_accounts').exists():
			return HttpResponseBadRequest('У вас уже максимальное количество ботов!')
		else:
			return func(*args, **kwargs)

	wrapper.__name__ = func.__name__
	return wrapper

def check_bot_id(func): # Декоратор для проверки ID бота
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]
		bot_id = kwargs['bot_id']

		bot = TelegramBotModel.objects.filter(owner_id=request.user.id)
		if bot.filter(id=bot_id).exists():
			bot = bot.get(id=bot_id)

			kwargs.update(
				{
					'bot': bot,
				}
			)

			return func(*args, **kwargs)
		else:
			return redirect(f'/account/constructor/{request.user.username}/')
	wrapper.__name__ = func.__name__
	return wrapper

def check_max_commands_count_for_account(func):
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]
		bot_id = kwargs['bot_id']

		if TelegramBotCommandModel.objects.filter(bot_id=bot_id).count() >= 15 and request.user.groups.filter(name='free_accounts').exists():
			return HttpResponseBadRequest('У вас уже максимальное количество команд!')
		else:
			return func(*args, **kwargs)

	wrapper.__name__ = func.__name__
	return wrapper

def check_command_id(func): # Декоратор для проверки ID команды бота
	def wrapper(*args, **kwargs):
		username, bot_id, command_id = kwargs['username'],  kwargs['bot_id'], kwargs['command_id']

		bot_command = TelegramBotCommandModel.objects.filter(bot_id=bot_id)
		if bot_command.filter(id=command_id).exists():
			bot_command = bot_command.get(id=command_id)

			kwargs.update(
				{
					'bot_command': bot_command,
				}
			)

			return func(*args, **kwargs)
		else:
			return redirect(f'/constructor/{username}/view_bot/{bot_id}/')
	wrapper.__name__ = func.__name__
	return wrapper