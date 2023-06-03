from django.test import TestCase, Client

from django.http import HttpResponse
from django import urls

from telegram_bot.models import TelegramBot, TelegramBotCommand, TelegramBotUser
from user.models import User

from functools import wraps
import json


class TelegramBotModelsTest(TestCase):
	def setUp(self) -> None:
		self.user: User = User.objects.create_user(user_id=123456789)
		self.telegram_bot: TelegramBot = TelegramBot.objects.add_telegram_bot(owner=self.user, api_token='123456789:qwertyuiop', is_private=True)

	def test_telegram_bot_model(self) -> None:
		self.assertEqual(TelegramBot.objects.count(), 1)

		self.assertEqual(self.telegram_bot.id, 1)
		self.assertEqual(self.telegram_bot.name, '123456789:qwertyuiop_test_telegram_bot')
		self.assertEqual(self.telegram_bot.api_token, '123456789:qwertyuiop')
		self.assertEqual(self.telegram_bot.is_private, True)
		self.assertEqual(self.telegram_bot.is_running, False)
		self.assertEqual(self.telegram_bot.is_stopped, True)

		self.telegram_bot.delete()
		self.assertEqual(TelegramBot.objects.count(), 0)

	# def test_telegram_bot_command_model(self) -> None:
	# 	self.assertEqual(self.telegram_bot.telegrambotcommand_set.count(), 0)
	# 	telegram_bot_command: TelegramBotCommand = TelegramBotCommand.objects.add_telegram_bot_command(
	# 		telegram_bot=self.telegram_bot,
	# 		name='Стартовая команда',
	# 		command='/start',
	# 		message_text='Привет ${username}!',
	# 		keyboard={
	# 			'type': 'default',
	# 			'buttons': ['Поддержка'],
	# 		},
	# 		api_request=['api_url', 'data']
	# 	)
	# 	self.assertEqual(self.telegram_bot.telegrambotcommand_set.count(), 1)

	# 	self.assertEqual(telegram_bot_command.id, 1)
	# 	self.assertEqual(telegram_bot_command.name, 'Стартовая команда')
	# 	self.assertEqual(telegram_bot_command.command, '/start')
	# 	self.assertEqual(telegram_bot_command.message_text, 'Привет ${username}!')
	# 	self.assertEqual(telegram_bot_command.api_request, ['api_url', 'data'])

	# 	self.assertEqual(telegram_bot_command.telegrambotcommandkeyboard_set.get().type, 'default')
	# 	self.assertEqual(telegram_bot_command.telegrambotcommandkeyboard_set.get().telegrambotcommandkeyboardbutton_set.get().name, 'Поддержка')

	def test_telegram_bot_user_model(self) -> None:
		self.assertEqual(self.telegram_bot.telegrambotuser_set.count(), 0)
		telegram_bot_user: TelegramBotUser = TelegramBotUser.objects.add_telegram_bot_user(
			telegram_bot=self.telegram_bot,
			user_id=12345,
			username='test'
		)
		self.assertEqual(self.telegram_bot.telegrambotuser_set.count(), 1)

		self.assertEqual(telegram_bot_user.id, 1)
		self.assertEqual(telegram_bot_user.user_id, 12345)
		self.assertEqual(telegram_bot_user.username, 'test')


class TelegramBotViewsTest(TestCase):
	def setUp(self) -> None:
		self.user: User = User.objects.create_user(user_id=123456789)

		self.client = Client(enforce_csrf_checks=True)

		self.telegram_bot: TelegramBot = TelegramBot.objects.add_telegram_bot(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=True
		)

	def test_add_telegram_bot_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('add_telegram_bot'),
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.post(
			urls.reverse('add_telegram_bot'),
			{},
			'application/json'
		)
		self.assertContains(response, 'В тело запроса переданы не все данные!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('add_telegram_bot'),
			{
				'api_token': '123456789:asdfghjkl',
			},
			'application/json'
		)
		self.assertContains(response, 'В тело запроса переданы не все данные!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('add_telegram_bot'),
			{
				'is_private': True,
			},
			'application/json'
		)
		self.assertContains(response, 'В тело запроса переданы не все данные!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('add_telegram_bot'),
			{
				'api_token': '',
				'is_private': True,
			},
			'application/json'
		)
		self.assertContains(response, 'Введите API-токен Telegram бота!', status_code=400)
		
		response: HttpResponse = self.client.post(
			urls.reverse('add_telegram_bot'),
			{
				'api_token': '123456789:asdfghjkl',
				'is_private': True,
			},
			'application/json'
		)
		self.assertContains(response, 'Вы успешно добавили Telegram бота.')

	def test_edit_telegram_bot_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('edit_telegram_bot', kwargs={'telegram_bot_id': 1}),
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse  = self.client.post(
			urls.reverse('edit_telegram_bot', kwargs={'telegram_bot_id': 0}),
			{
				'is_private': False
			},
			'application/json'
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse  = self.client.post(
			urls.reverse('edit_telegram_bot', kwargs={'telegram_bot_id': 1}),
			{
				'is_private': False
			},
			'application/json'
		)
		self.assertContains(response, 'Вы успешно изменили Telegram бота.')

	# def test_add_telegram_bot_command_view(self) -> None:
	# 	response = self.client.post(
	# 		urls.reverse('add_telegram_bot_command', kwargs={'telegram_bot_id': 1}),
	# 		{
	# 			'name': 'Стартовая команда',
	# 			'command': '/start',
	# 			'message_text': 'Привет ${username}!',
	# 			'keyboard': ['offKeyboard'],
	# 		},
	# 		'application/json'
	# 	)
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertContains(response, 'Вы успешно добавили команду Telegram боту.')

	# def add_telegram_bot_command(func):
	# 	@wraps(func)
	# 	def wrapper(*args, **kwargs):
	# 		self = args[0]

	# 		TelegramBotCommand.objects.add_telegram_bot_command(
	# 			telegram_bot=self.telegram_bot,
	# 			name='Стартовая команда',
	# 			command='/start',
	# 			message_text='Привет ${username}!',
	# 			keyboard=['offKeyboard']
	# 		)

	# 		return func(*args, **kwargs)
	# 	return wrapper
	
	# @add_telegram_bot_command
	# def test_get_telegram_bot_command_data_view(self) -> None:
	# 	response = self.client.post(
	# 		urls.reverse('get_telegram_bot_command_data', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
	# 		{},
	# 		'application/json'
	# 	)
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertJSONEqual(
	# 		response.content,
	# 		json.dumps(
	# 			{
	# 				'name': 'Стартовая команда',
	# 				'command': '/start',
	# 				'message_text': 'Привет ${username}!',
	# 				'keyboard': ['offKeyboard'],
	# 			}
	# 		)
	# 	)

	# @add_telegram_bot_command
	# def test_edit_telegram_bot_command_view(self) -> None:	
	# 	response = self.client.post(
	# 		urls.reverse('edit_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
	# 		{
	# 			'name': 'Стартовая команда',
	# 			'command': '/start',
	# 			'message_text': 'Привет ${username}!',
	# 			'keyboard': ['offKeyboard'],
	# 		},
	# 		'application/json'
	# 	)
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertContains(response, 'Вы успешно изменили команду Telegram бота.')

	# @add_telegram_bot_command
	# def test_delete_telegram_bot_command_view(self) -> None:
	# 	response = self.client.post(
	# 		urls.reverse('delete_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
	# 		{},
	# 		'application/json'
	# 	)
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertContains(response, 'Вы успешно удалили команду Telegram бота.')

	def add_telegram_bot_user(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			self = args[0]

			TelegramBotUser.objects.add_telegram_bot_user(telegram_bot=self.telegram_bot, user_id=12345, username='test')

			return func(*args, **kwargs)
		return wrapper

	@add_telegram_bot_user
	def test_add_allowed_user_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('add_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1}),
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.post(
			urls.reverse('add_allowed_user', kwargs={'telegram_bot_id': 0, 'telegram_bot_user_id': 1}),
			{},
			'application/json'
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('add_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 0}),
			{},
			'application/json'
		)
		self.assertContains(response, 'Пользователь Telegram бота не найдена!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('add_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1}),
			{},
			'application/json'
		)
		self.assertContains(response, 'Вы успешно добавили пользователя в список разрешённых пользователей Telegram бота.')

	@add_telegram_bot_user
	def test_delete_allowed_user_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('delete_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1}),
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_allowed_user', kwargs={'telegram_bot_id': 0, 'telegram_bot_user_id': 1}),
			{},
			'application/json'
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 0}),
			{},
			'application/json'
		)
		self.assertContains(response, 'Пользователь Telegram бота не найдена!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1}),
			{},
			'application/json'
		)
		self.assertContains(response, 'Вы успешно удалили пользователя из списка разрешённых пользователей Telegram бота.')

	@add_telegram_bot_user
	def test_delete_telegram_bot_user_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('delete_telegram_bot_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1}),
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_telegram_bot_user', kwargs={'telegram_bot_id': 0, 'telegram_bot_user_id': 1}),
			{},
			'application/json'
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_telegram_bot_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 0}),
			{},
			'application/json'
		)
		self.assertContains(response, 'Пользователь Telegram бота не найдена!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_telegram_bot_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1}),
			{},
			'application/json'
		)
		self.assertContains(response, 'Вы успешно удалили пользователя Telegram бота.')


	# @add_telegram_bot_command
	# def test_get_telegram_bot_commands_view(self) -> None:
	# 	response = self.client.post(
	# 		urls.reverse('get_telegram_bot_commands', kwargs={'telegram_bot_id': 1}),
	# 		{},
	# 		'application/json'
	# 	)
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertJSONEqual(
	# 		response.content,
	# 		json.dumps(
	# 			{
	# 				'commands_count': 1,
	# 				'commands': [
	# 					{
	# 						'id': 1,
	# 						'name': 'Стартовая команда',
	# 					},
	# 				],
	# 			}
	# 		)
	# 	)

	@add_telegram_bot_user
	def test_get_telegram_bot_users_view(self) -> None:
		telegram_bot_user: TelegramBotUser = TelegramBotUser.objects.get(id=1)

		response: HttpResponse = self.client.post(
			urls.reverse('get_telegram_bot_users', kwargs={'telegram_bot_id': 1}),
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.post(
			urls.reverse('get_telegram_bot_users', kwargs={'telegram_bot_id': 0}),
			{},
			'application/json'
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('get_telegram_bot_users', kwargs={'telegram_bot_id': 1}),
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(
			response.content,
			json.dumps(
				{
					'users_count': 1,
					'users': [
						{
							'id': 1,
							'username': 'test',
							'is_allowed': False,
							'date_activated': telegram_bot_user.date_activated,
						},
					],
				}
			)
		)
