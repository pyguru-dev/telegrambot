from telegram_bot.services.tests import CustomTestCase

from telegram_bot.services.custom_aiogram import CustomBot

from user.models import User

from telegram_bot.services import ConstructorTelegramBot

from functools import wraps


class ConstructorTelegramBotTests(CustomTestCase):
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
		results: list = await self.send_message(self.constructor_telegram_bot.start_command, '/start')
		assert len(results) == 1
		assert results[0]['method'] == 'send_message'
		assert results[0]['text'] == f"""\
			Привет, @test!
			Я являюсь Telegram ботом для сайта Constructor Telegram Bots.
			Спасибо за то, что ты с нами ❤️
		""".replace('	', '')

	@setup
	async def test_login_command(self):
		results: list = await self.send_message(self.constructor_telegram_bot.login_command, '/login')

		user: User = await User.objects.afirst()
		login_url: str = await user.alogin_url

		assert len(results) == 1
		assert results[0]['method'] == 'send_message'
		assert results[0]['text'] == 'Нажмите на кнопку ниже, чтобы авторизоваться на сайте.'
		assert results[0]['reply_markup']['inline_keyboard'][0][0]['text'] == 'Авторизация'
		assert results[0]['reply_markup']['inline_keyboard'][0][0]['url'] == login_url
