from django.test import TestCase, Client

from django.http import HttpResponse
from django import urls

from telegram_bot.models import (
	TelegramBot,
	TelegramBotCommand, TelegramBotCommandKeyboard,
	TelegramBotUser
)
from user.models import User

from functools import wraps
import json


class TelegramBotModelsTest(TestCase):
	def setUp(self) -> None:
		self.user: User = User.objects.create_user(user_id=123456789)
		self.telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=True
		)

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

	def test_telegram_bot_command_model(self) -> None:
		self.assertEqual(self.telegram_bot.commands.count(), 0)
		telegram_bot_command: TelegramBotCommand = TelegramBotCommand.objects.create(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда 1',
			message_text='Привет!',
			command='/start',
			api_request=['api_url', 'data']
		)
		self.assertEqual(self.telegram_bot.commands.count(), 1)

		self.assertEqual(telegram_bot_command.id, 1)
		self.assertEqual(telegram_bot_command.name, 'Стартовая команда 1')
		self.assertEqual(telegram_bot_command.command, '/start')
		self.assertEqual(str(telegram_bot_command.image), '')
		self.assertEqual(telegram_bot_command.message_text, 'Привет!')
		self.assertEqual(telegram_bot_command.api_request, ['api_url', 'data'])

		self.assertEqual(telegram_bot_command.x, 0)
		self.assertEqual(telegram_bot_command.y, 0)

		self.assertEqual(self.telegram_bot.commands.count(), 1)
		telegram_bot_command: TelegramBotCommand = TelegramBotCommand.objects.create(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда 2',
			message_text='Привет!',
		)
		self.assertEqual(self.telegram_bot.commands.count(), 2)

		self.assertEqual(telegram_bot_command.id, 2)
		self.assertEqual(telegram_bot_command.name, 'Стартовая команда 2')
		self.assertEqual(telegram_bot_command.command, None)
		self.assertEqual(str(telegram_bot_command.image), '')
		self.assertEqual(telegram_bot_command.message_text, 'Привет!')
		self.assertEqual(telegram_bot_command.api_request, None)

		self.assertEqual(telegram_bot_command.x, 0)
		self.assertEqual(telegram_bot_command.y, 0)

	def test_test_telegram_bot_command_keyboard_model(self) -> None:
		telegram_bot_command: TelegramBotCommand = TelegramBotCommand.objects.create(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда',
			message_text='Привет!',
			command='/start',
			keyboard={
				'type': 'default',
				'buttons': [
					{
						'id': '',
						'text': 'Поддержка'
					}
				],
			},
			api_request=['api_url', 'data']
		)

		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = telegram_bot_command.get_keyboard()
		self.assertEqual(telegram_bot_command_keyboard, telegram_bot_command.keyboard)
		self.assertEqual(telegram_bot_command_keyboard.type, 'default')

		telegram_bot_command_keyboard_button = telegram_bot_command_keyboard.buttons.first()
		self.assertEqual(telegram_bot_command_keyboard_button.text, 'Поддержка')
		self.assertEqual(telegram_bot_command_keyboard_button.telegram_bot_command, None)
		self.assertEqual(telegram_bot_command_keyboard_button.start_diagram_connector, None)
		self.assertEqual(telegram_bot_command_keyboard_button.end_diagram_connector, None)

	def test_telegram_bot_user_model(self) -> None:
		self.assertEqual(self.telegram_bot.users.count(), 0)
		telegram_bot_user: TelegramBotUser = TelegramBotUser.objects.create(
			telegram_bot=self.telegram_bot,
			user_id=12345,
			username='test'
		)
		self.assertEqual(self.telegram_bot.users.count(), 1)

		self.assertEqual(telegram_bot_user.id, 1)
		self.assertEqual(telegram_bot_user.user_id, 12345)
		self.assertEqual(telegram_bot_user.username, 'test')


class TelegramBotViewsTest(TestCase):
	def setUp(self) -> None:
		self.user: User = User.objects.create_user(user_id=123456789)

		self.client = Client(enforce_csrf_checks=True)

		self.telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=True
		)

	def test_add_telegram_bot_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('add_telegram_bot')
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)
		
		response: HttpResponse = self.client.post(
			urls.reverse('add_telegram_bot'),
			{
				'api_token': '123456789:asdfghjkl',
				'is_private': True,
			},
			'application/json'
		)
		self.assertContains(response, 'Вы успешно добавили Telegram бота.')

	def test_edit_telegram_bot_api_token_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('edit_telegram_bot_api_token', kwargs={'telegram_bot_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse  = self.client.post(
			urls.reverse('edit_telegram_bot_api_token', kwargs={'telegram_bot_id': 0}),
			{
				'api_token': '123456789:dwawdadwa',
			},
			'application/json'
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse  = self.client.post(
			urls.reverse('edit_telegram_bot_api_token', kwargs={'telegram_bot_id': 1}),
			{
				'api_token': '123456789:qwertyuiop',
			},
			'application/json'
		)
		self.assertContains(response, 'Вы уже используете этот API-токен Telegram бота на сайте!', status_code=400)

		response: HttpResponse  = self.client.post(
			urls.reverse('edit_telegram_bot_api_token', kwargs={'telegram_bot_id': 1}),
			{
				'api_token': '123456789:dwawdadwa',
			},
			'application/json'
		)
		self.assertContains(response, 'Вы успешно изменили API-токен Telegram бота.')

	def test_edit_telegram_bot_private_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('edit_telegram_bot_private', kwargs={'telegram_bot_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse  = self.client.post(
			urls.reverse('edit_telegram_bot_private', kwargs={'telegram_bot_id': 0}),
			{
				'is_private': False
			},
			'application/json'
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse  = self.client.post(
			urls.reverse('edit_telegram_bot_private', kwargs={'telegram_bot_id': 1}),
			{
				'is_private': False
			},
			'application/json'
		)
		self.assertContains(response, 'Вы успешно сделали Telegram бота не приватным.')

	def test_delete_telegram_bot_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('delete_telegram_bot', kwargs={'telegram_bot_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse  = self.client.post(
			urls.reverse('delete_telegram_bot', kwargs={'telegram_bot_id': 0})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_telegram_bot', kwargs={'telegram_bot_id': 1})
		)
		self.assertContains(response, 'Вы успешно удалили Telegram бота.')


	def test_get_telegram_bot_data_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('get_telegram_bot_data', kwargs={'telegram_bot_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse  = self.client.post(
			urls.reverse('get_telegram_bot_data', kwargs={'telegram_bot_id': 0})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)
		
		response = self.client.post(
			urls.reverse('get_telegram_bot_data', kwargs={'telegram_bot_id': 1})
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(
			response.content,
			json.dumps(
				{
					'id': 1,
					'name': '123456789:qwertyuiop_test_telegram_bot',
					'api_token': '123456789:qwertyuiop',
					'is_running': False,
					'is_stopped': True,
					'commands_count': 0,
					'users_count': 0,
					'date_added': self.telegram_bot.date_added,
				}
			)
		)


	def test_add_telegram_bot_command_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('add_telegram_bot_command', kwargs={'telegram_bot_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse  = self.client.post(
			urls.reverse('add_telegram_bot_command', kwargs={'telegram_bot_id': 0})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response = self.client.post(
			urls.reverse('add_telegram_bot_command', kwargs={'telegram_bot_id': 1}),
			{
				'image': 'null',
				'name': 'Стартовая команда',
				'command': None,
				'message_text': 'Привет!',
				'keyboard': None,
				'api_request': None,
			},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно добавили команду Telegram боту.')

	def add_telegram_bot_command(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			self = args[0]

			TelegramBotCommand.objects.create(
				telegram_bot=self.telegram_bot,
				name='Стартовая команда',
				message_text='Привет',
			)

			return func(*args, **kwargs)
		return wrapper

	@add_telegram_bot_command
	def test_edit_telegram_bot_command_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('edit_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse  = self.client.post(
			urls.reverse('edit_telegram_bot_command', kwargs={'telegram_bot_id': 0, 'telegram_bot_command_id': 1})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse  = self.client.post(
			urls.reverse('edit_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 0})
		)
		self.assertContains(response, 'Команда Telegram бота не найдена!', status_code=400)

		response = self.client.post(
			urls.reverse('edit_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
			{
				'image': 'null',
				'name': 'Стартовая команда',
				'command': None,
				'message_text': 'Привет!',
				'keyboard': None,
				'api_request': None,
			},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно изменили команду Telegram бота.')

	@add_telegram_bot_command
	def test_delete_telegram_bot_command_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('delete_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse  = self.client.post(
			urls.reverse('delete_telegram_bot_command', kwargs={'telegram_bot_id': 0, 'telegram_bot_command_id': 1})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse  = self.client.post(
			urls.reverse('delete_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 0})
		)
		self.assertContains(response, 'Команда Telegram бота не найдена!', status_code=400)

		response = self.client.post(
			urls.reverse('delete_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1})
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно удалили команду Telegram бота.')


	@add_telegram_bot_command
	def test_get_telegram_bot_command_data_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('get_telegram_bot_command_data', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse  = self.client.post(
			urls.reverse('get_telegram_bot_command_data', kwargs={'telegram_bot_id': 0, 'telegram_bot_command_id': 1})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse  = self.client.post(
			urls.reverse('get_telegram_bot_command_data', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 0})
		)
		self.assertContains(response, 'Команда Telegram бота не найдена!', status_code=400)

		response = self.client.post(
			urls.reverse('get_telegram_bot_command_data', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1})
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(
			response.content,
			json.dumps(
				{
					'id': 1,
					'name': 'Стартовая команда',
					'command': None,
					'image': '',
					'message_text': 'Привет',
					'keyboard': None,
					'api_request': None,

					'x': 0,
					'y': 0,
				}
			)
		)

	def add_telegram_bot_user(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			self = args[0]

			TelegramBotUser.objects.create(
				telegram_bot=self.telegram_bot,
				user_id=12345,
				username='test'
			)

			return func(*args, **kwargs)
		return wrapper

	@add_telegram_bot_user
	def test_add_allowed_user_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('add_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.post(
			urls.reverse('add_allowed_user', kwargs={'telegram_bot_id': 0, 'telegram_bot_user_id': 1})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('add_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 0})
		)
		self.assertContains(response, 'Пользователь Telegram бота не найдена!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('add_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1})
		)
		self.assertContains(response, 'Вы успешно добавили пользователя в список разрешённых пользователей Telegram бота.')

	@add_telegram_bot_user
	def test_delete_allowed_user_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('delete_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_allowed_user', kwargs={'telegram_bot_id': 0, 'telegram_bot_user_id': 1})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 0})
		)
		self.assertContains(response, 'Пользователь Telegram бота не найдена!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1})
		)
		self.assertContains(response, 'Вы успешно удалили пользователя из списка разрешённых пользователей Telegram бота.')

	@add_telegram_bot_user
	def test_delete_telegram_bot_user_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('delete_telegram_bot_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_telegram_bot_user', kwargs={'telegram_bot_id': 0, 'telegram_bot_user_id': 1})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_telegram_bot_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 0})
		)
		self.assertContains(response, 'Пользователь Telegram бота не найдена!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('delete_telegram_bot_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1})
		)
		self.assertContains(response, 'Вы успешно удалили пользователя Telegram бота.')


	def test_save_telegram_bot_diagram_current_scale(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('save_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.post(
			urls.reverse('save_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': 0})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)
		
		response = self.client.post(
			urls.reverse('save_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': 1}),
			{
				'diagram_current_scale': 1.0,
			},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)

	@add_telegram_bot_command
	def test_save_telegram_bot_command_position(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('save_telegram_bot_command_position', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse  = self.client.post(
			urls.reverse('save_telegram_bot_command_position', kwargs={'telegram_bot_id': 0, 'telegram_bot_command_id': 1})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse  = self.client.post(
			urls.reverse('save_telegram_bot_command_position', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 0})
		)
		self.assertContains(response, 'Команда Telegram бота не найдена!', status_code=400)
		
		response = self.client.post(
			urls.reverse('save_telegram_bot_command_position', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
			{
				'x': 10,
				'y': 50,
			},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)


	@add_telegram_bot_command
	def test_get_telegram_bot_commands_view(self) -> None:
		response: HttpResponse = self.client.post(
			urls.reverse('get_telegram_bot_commands', kwargs={'telegram_bot_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.post(
			urls.reverse('get_telegram_bot_commands', kwargs={'telegram_bot_id': 0})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)
		
		response = self.client.post(
			urls.reverse('get_telegram_bot_commands', kwargs={'telegram_bot_id': 1})
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(
			response.content,
			json.dumps(
				[
					{
						'id': 1,
						'name': 'Стартовая команда',
						'command': None,
						'image': '',
						'message_text': 'Привет',
						'keyboard': None,
						'api_request': None,

						'x': 0,
						'y': 0,
					},
				]
			)
		)

	@add_telegram_bot_user
	def test_get_telegram_bot_users_view(self) -> None:
		telegram_bot_user: TelegramBotUser = TelegramBotUser.objects.get(id=1)

		response: HttpResponse = self.client.post(
			urls.reverse('get_telegram_bot_users', kwargs={'telegram_bot_id': 1})
		)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.post(
			urls.reverse('get_telegram_bot_users', kwargs={'telegram_bot_id': 0})
		)
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response: HttpResponse = self.client.post(
			urls.reverse('get_telegram_bot_users', kwargs={'telegram_bot_id': 1})
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(
			response.content,
			json.dumps(
				[
					{
						'id': 1,
						'user_id': 12345,
						'username': 'test',
						'is_allowed': False,
						'date_activated': telegram_bot_user.date_activated,
					},
				]
			)
		)
