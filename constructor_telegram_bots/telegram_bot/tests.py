from django.test import TestCase, Client

from telegram_bot.models import TelegramBot, TelegramBotCommand, TelegramBotUser
from user.models import User

import json


class TelegramBotModelsTest(TestCase):
	def setUp(self) -> None:
		self.user = User.objects.create_user(user_id=123456789)
		self.telegram_bot = TelegramBot.objects.add_telegram_bot(user=self.user, api_token='123456789:qwertyuiop', is_private=True)

	def test_telegram_bot_model(self) -> None:
		self.assertEqual(self.telegram_bot.id, 1)
		self.assertEqual(self.telegram_bot.name, '123456789:qwertyuiop_test_telegram_bot')
		self.assertEqual(self.telegram_bot.api_token, '123456789:qwertyuiop')
		self.assertEqual(self.telegram_bot.is_private, True)
		self.assertEqual(self.telegram_bot.is_running, False)
		self.assertEqual(self.telegram_bot.is_stopped, True)

		self.assertEqual(self.telegram_bot.commands.count(), 0)
		self.assertEqual(self.telegram_bot.users.count(), 0)
		TelegramBotCommand.objects.add_telegram_bot_command(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда',
			command='/start',
			callback='',
			message_text='Привет ${username}!',
			keyboard=['offKeyboard']
		)
		TelegramBotUser.objects.add_telegram_bot_user(telegram_bot=self.telegram_bot, user_id=12345, username='test')
		self.assertEqual(self.telegram_bot.commands.count(), 1)
		self.assertEqual(self.telegram_bot.users.count(), 1)

		self.assertEqual(TelegramBot.objects.count(), 1)
		duplicated_telegram_bot = self.telegram_bot.duplicate(user=self.user, api_token='123456789:asdfghjkl', is_private=False)
		self.assertEqual(TelegramBot.objects.count(), 2)

		self.assertEqual(duplicated_telegram_bot.id, 2)
		self.assertEqual(duplicated_telegram_bot.name, '123456789:asdfghjkl_test_telegram_bot')
		self.assertEqual(duplicated_telegram_bot.api_token, '123456789:asdfghjkl')
		self.assertEqual(duplicated_telegram_bot.is_private, False)
		self.assertEqual(duplicated_telegram_bot.is_running, False)
		self.assertEqual(duplicated_telegram_bot.is_stopped, True)
		self.assertEqual(duplicated_telegram_bot.commands.count(), 1)
		self.assertEqual(duplicated_telegram_bot.users.count(), 0)

		self.assertEqual(TelegramBot.objects.count(), 2)
		self.assertEqual(TelegramBotCommand.objects.count(), 2)
		self.assertEqual(TelegramBotUser.objects.count(), 1)
		self.telegram_bot.delete()
		self.assertEqual(TelegramBot.objects.count(), 1)
		self.assertEqual(TelegramBotCommand.objects.count(), 1)
		self.assertEqual(TelegramBotUser.objects.count(), 0)

	def test_telegram_bot_command_model(self) -> None:
		self.assertEqual(self.telegram_bot.commands.count(), 0)
		telegram_bot_command = TelegramBotCommand.objects.add_telegram_bot_command(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда',
			command='/start',
			callback='',
			message_text='Привет ${username}!',
			keyboard=['offKeyboard']
		)
		self.assertEqual(self.telegram_bot.commands.count(), 1)

		self.assertEqual(telegram_bot_command.id, 1)
		self.assertEqual(telegram_bot_command.name, 'Стартовая команда')
		self.assertEqual(telegram_bot_command.command, '/start')
		self.assertEqual(telegram_bot_command.callback, '')
		self.assertEqual(telegram_bot_command.message_text, 'Привет ${username}!')
		self.assertEqual(telegram_bot_command.keyboard, ['offKeyboard'])

	def test_telegram_bot_user_model(self) -> None:
		self.assertEqual(self.telegram_bot.users.count(), 0)
		telegram_bot_user = TelegramBotUser.objects.add_telegram_bot_user(telegram_bot=self.telegram_bot, user_id=12345, username='test')
		self.assertEqual(self.telegram_bot.users.count(), 1)

		self.assertEqual(telegram_bot_user.id, 1)
		self.assertEqual(telegram_bot_user.user_id, 12345)
		self.assertEqual(telegram_bot_user.username, 'test')


class TelegramBotViewsTest(TestCase):
	def setUp(self) -> None:
		self.user = User.objects.create_user(user_id=123456789)
		login_url = self.user.get_login_url()

		self.client = Client(enforce_csrf_checks=True)
		self.client.get(login_url)

		self.telegram_bot = TelegramBot.objects.add_telegram_bot(user=self.user, api_token='123456789:qwertyuiop', is_private=True)

	def test_add_telegram_bot_view(self) -> None:
		response = self.client.post(
			'/telegram-bot/add/',
			{
				'api_token': '123456789:asdfghjkl',
				'is_private': True,
			},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно добавили Telegram бота.')

	def test_edit_telegram_bot_view(self) -> None:
		response = self.client.post(
			'/telegram-bot/1/edit/',
			{
				'is_private': False
			},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно изменили Telegram бота.')

	def test_duplicate_telegram_bot_view(self) -> None:
		response = self.client.post(
			'/telegram-bot/1/duplicate/',
			{
				'api_token': '123456789:asdfghjkl',
				'is_private': True,
			},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно дублировали Telegram бота.')

	def test_duplicate_telegram_bot_view(self) -> None:
		response = self.client.post(
			'/telegram-bot/1/delete/',
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно удалили Telegram бота.')


	def test_add_telegram_bot_command_view(self) -> None:
		response = self.client.post(
			'/telegram-bot/1/command/add/',
			{
				'name': 'Стартовая команда',
				'command': '/start',
				'callback': '',
				'message_text': 'Привет ${username}!',
				'keyboard': ['offKeyboard'],
			},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно добавили команду Telegram боту.')

	def add_telegram_bot_command(func):
		def wrapper(*args, **kwargs):
			self = args[0]

			TelegramBotCommand.objects.add_telegram_bot_command(
				telegram_bot=self.telegram_bot,
				name='Стартовая команда',
				command='/start',
				callback='',
				message_text='Привет ${username}!',
				keyboard=['offKeyboard']
			)

			return func(*args, **kwargs)
		return wrapper
	
	@add_telegram_bot_command
	def test_get_telegram_bot_command_data_view(self) -> None:
		response = self.client.post(
			'/telegram-bot/1/command/1/get-data/',
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(
			response.content,
			json.dumps(
				{
					'name': 'Стартовая команда',
					'command': '/start',
					'callback': '',
					'message_text': 'Привет ${username}!',
					'keyboard': ['offKeyboard'],
				}
			)
		)

	@add_telegram_bot_command
	def test_edit_telegram_bot_command_view(self) -> None:	
		response = self.client.post(
			'/telegram-bot/1/command/1/edit/',
			{
				'name': 'Стартовая команда',
				'command': '/start',
				'callback': '',
				'message_text': 'Привет ${username}!',
				'keyboard': ['offKeyboard'],
			},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно изменили команду Telegram бота.')

	@add_telegram_bot_command
	def test_delete_telegram_bot_command_view(self) -> None:
		response = self.client.post(
			'/telegram-bot/1/command/1/delete/',
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно удалили команду Telegram бота.')

	def add_telegram_bot_user(func):
		def wrapper(*args, **kwargs):
			self = args[0]

			TelegramBotUser.objects.add_telegram_bot_user(telegram_bot=self.telegram_bot, user_id=12345, username='test')

			return func(*args, **kwargs)
		return wrapper

	@add_telegram_bot_user
	def test_add_allowed_user_view(self) -> None:
		response = self.client.post(
			'/telegram-bot/1/user/1/add-allowed-user/',
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно добавили пользователя в список разрешённых пользователей Telegram бота.')

	@add_telegram_bot_user
	def test_delete_allowed_user_view(self) -> None:
		response = self.client.post(
			'/telegram-bot/1/user/1/delete-allowed-user/',
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно удалили пользователя из списка разрешённых пользователей Telegram бота.')

	@add_telegram_bot_user
	def test_delete_telegram_bot_user_view(self) -> None:
		response = self.client.post(
			'/telegram-bot/1/user/1/delete/',
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Вы успешно удалили пользователя Telegram бота.')


	@add_telegram_bot_command
	def test_get_telegram_bot_commands_view(self) -> None:
		response = self.client.post(
			'/telegram-bot/1/get-commands/',
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(
			response.content,
			json.dumps(
				{
					'commands_count': 1,
					1: 'Стартовая команда',
				}
			)
		)

	@add_telegram_bot_user
	def test_get_telegram_bot_users_view(self) -> None:
		telegram_bot_user = TelegramBotUser.objects.get(id=1)

		response = self.client.post(
			'/telegram-bot/1/get-users/',
			{},
			'application/json'
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(
			response.content,
			json.dumps(
				{
					'users_count': 1,
					1: {
						'username': 'test',
						'is_allowed': False,
						'date_started': telegram_bot_user.get_date_started(),
					},
				}
			)
		)
