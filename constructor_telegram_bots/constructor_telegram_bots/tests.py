from django.test import TestCase, Client
from django.http import HttpResponse

from user.models import User
from telegram_bot.models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandKeyboard,
	TelegramBotUser
)


class BaseTestCase(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)
		
		self.user: User = User.objects.create_user(user_id=123456789)
		self.telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=True
		)
		self.telegram_bot_command: TelegramBotCommand = TelegramBotCommand.objects.create(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда',
			message_text='Привет!'
		)
		self.telegram_bot_command_keyboard: TelegramBotCommandKeyboard = TelegramBotCommandKeyboard.objects.create(
			telegram_bot_command=self.telegram_bot_command,
			type='defualt',
			buttons=[
				{
					'text': '1',
					'url': 'http://example.com/',
				},
				{
					'text': '2',
					'url': None,
				},
			]
		)
		self.telegram_bot_user: TelegramBotUser = TelegramBotUser.objects.create(
			telegram_bot=self.telegram_bot,
			user_id=123456789,
			full_name='Test A'
		)

	def assertUnauthorizedAccess(self, url: str, method: str = 'POST'):
		if method == 'POST':
			response: HttpResponse = self.client.post(url)
		else:
			response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

	def assertTests(self, tests: list):
		for test in tests:
			if 'data' in test:
				response: HttpResponse = self.client.post(test['url'], test['data'], 'application/json')
			else:
				response: HttpResponse = self.client.post(test['url'])

			if 'response' in test:
				self.assertJSONEqual(response.content, test['response'])
