from telegram_bot.services.tests import BaseTestCase
from telegram_bot.services.custom_aiogram import CustomBot

from user.models import User

from .telegram_bot import ConstructorTelegramBot

from functools import wraps
import json


class ConstructorTelegramBotTests(BaseTestCase):
	def setUp(self) -> None:
		self.constructor_telegram_bot = ConstructorTelegramBot()

	def setup(func):
		wraps(func)
		async def wrapper(self, *args, **kwargs):
			await self.constructor_telegram_bot.setup()

			self.bot: CustomBot = self.constructor_telegram_bot.bot

			return await func(self, *args, **kwargs)
		return wrapper

	@setup
	async def test_start_command(self):
		result: dict = (await self.send_message(self.constructor_telegram_bot.start_command, '/start'))[0]

		assert result['method'] == 'sendMessage'
		assert result['text'] == f"""\
			Hello, @test!
			I am a Telegram bot for Constructor Telegram Bots site.
			Thank you for being with us ❤️
		""".replace('\t', '')

	@setup
	async def test_login_command(self):
		result: dict = (await self.send_message(self.constructor_telegram_bot.login_command, '/login'))[0]
		result_keyboard: dict = json.loads(result['reply_markup'])['inline_keyboard']

		user: User = await User.objects.afirst()
		login_url: str = await user.alogin_url

		assert result['method'] == 'sendMessage'
		assert result['text'] == 'Click on the button below to login on the site.'
		assert result_keyboard[0][0]['text'] == 'Login'
		assert result_keyboard[0][0]['url'] == login_url
