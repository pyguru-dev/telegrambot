from django.test import TestCase, Client

from user.models import User
from telegram_bot.models import TelegramBot, TelegramBotCommand, TelegramBotCommandKeyboard, TelegramBotUser


class BaseTestCase(TestCase):
	def setUp(self) -> None:
		self.maxDiff = None
		self.client = Client(enforce_csrf_checks=True)

		self.user: User = User.objects.create(telegram_id=123456789, first_name='exg1o')
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
					'row': None,
					'text': '1',
					'url': 'http://example.com/',
				},
				{
					'row': None,
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
