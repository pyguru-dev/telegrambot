from telegram_bot.services.tests import CustomTestCase

from telegram_bot.services.custom_aiogram import CustomBot

from user.models import User
from telegram_bot.models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton
)

from telegram_bot.services import UserTelegramBot

from asgiref.sync import sync_to_async

from functools import wraps


class UserTelegramBotTests(CustomTestCase):
	def setUp(self) -> None:
		self.user: User = User.objects.create_user(user_id=123456789)
		self.telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=False
		)

		self.user_telegram_bot = UserTelegramBot(telegram_bot=self.telegram_bot)
		self.handler = self.user_telegram_bot.message_and_callback_query_handler

	def setup(func):
		wraps(func)
		async def wrapper(self, *args, **kwargs):
			await self.user_telegram_bot.setup()

			self.bot: CustomBot = self.user_telegram_bot.bot

			return await func(self, *args, **kwargs)
		return wrapper

	@setup
	async def test_send_message(self) -> None:
		assert not await self.send_message(self.handler, 'Hello')

	@setup
	async def test_send_command(self) -> None:
		telegram_bot_command: TelegramBotCommand = await sync_to_async(TelegramBotCommand.objects.create)(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда',
			command='/start',
			message_text='Это стартовая команда'
		)

		results: list = await self.send_message(self.handler,  telegram_bot_command.command)

		assert len(results) == 1
		assert results[0]['method'] == 'send_message'
		assert results[0]['text'] == telegram_bot_command.message_text
		assert results[0]['reply_markup'] == None

	@setup
	async def test_send_command_with_default_keyboard(self) -> None:
		telegram_bot_command: TelegramBotCommand = await sync_to_async(TelegramBotCommand.objects.create)(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда',
			command='/start',
			message_text='Это стартовая команда',
			keyboard={
				'type': 'default',
				'buttons': [
					{
						'row': None,

						'text': '1',
						'url': None,
					},
					{
						'row': 2,

						'text': '2',
						'url': None,
					},
					{
						'row': 2,

						'text': '3',
						'url': None,
					},
				],
			}
		)

		results: list = await self.send_message(self.handler,  telegram_bot_command.command)

		assert len(results) == 1
		assert results[0]['method'] == 'send_message'
		assert results[0]['text'] == telegram_bot_command.message_text
		assert results[0]['reply_markup']['keyboard'][0][0]['text'] == '1'
		assert results[0]['reply_markup']['keyboard'][1][0]['text'] == '2'
		assert results[0]['reply_markup']['keyboard'][1][1]['text'] == '3'

	@setup
	async def test_send_command_with_inline_keyboard(self) -> None:
		telegram_bot_command: TelegramBotCommand = await sync_to_async(TelegramBotCommand.objects.create)(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда',
			command='/start',
			message_text='Это стартовая команда',
			keyboard={
				'type': 'inline',
				'buttons': [
					{
						'row': None,

						'text': '1',
						'url': 'https://example.com/',
					},
				],
			}
		)

		results: list = await self.send_message(self.handler,  telegram_bot_command.command)

		assert len(results) == 1
		assert results[0]['method'] == 'send_message'
		assert results[0]['text'] == telegram_bot_command.message_text
		assert results[0]['reply_markup']['inline_keyboard'][0][0]['text'] == '1'
		assert results[0]['reply_markup']['inline_keyboard'][0][0]['url'] == 'https://example.com/'

	@setup
	async def test_click_default_keyboard_button(self) -> None:
		telegram_bot_command_1: TelegramBotCommand = await sync_to_async(TelegramBotCommand.objects.create)(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда',
			command='/start',
			message_text='Это стартовая команда',
			keyboard={
				'type': 'default',
				'buttons': [
					{
						'row': None,

						'text': '1',
						'url': None,
					},
				],
			}
		)

		telegram_bot_command_2: TelegramBotCommand = await sync_to_async(TelegramBotCommand.objects.create)(
			telegram_bot=self.telegram_bot,
			name='Нажал на кнопку',
			message_text='Ты нажал на кнопку!',
		)

		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = await sync_to_async(telegram_bot_command_1.get_keyboard)()

		telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton = await telegram_bot_command_keyboard.buttons.afirst()
		telegram_bot_command_keyboard_button.telegram_bot_command = telegram_bot_command_2
		await telegram_bot_command_keyboard_button.asave()

		results: list = await self.send_message(self.handler,  '1')
		assert len(results) == 1
		assert results[0]['method'] == 'send_message'
		assert results[0]['text'] == telegram_bot_command_2.message_text

	@setup
	async def test_click_inline_keyboard_button(self) -> None:
		telegram_bot_command_1: TelegramBotCommand = await sync_to_async(TelegramBotCommand.objects.create)(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда',
			command='/start',
			message_text='Это стартовая команда',
			keyboard={
				'type': 'inline',
				'buttons': [
					{
						'row': None,

						'text': '1',
						'url': None,
					},
				],
			}
		)

		telegram_bot_command_2: TelegramBotCommand = await sync_to_async(TelegramBotCommand.objects.create)(
			telegram_bot=self.telegram_bot,
			name='Нажал на кнопку',
			message_text='Ты нажал на кнопку!',
		)

		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = await sync_to_async(telegram_bot_command_1.get_keyboard)()

		telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton = await telegram_bot_command_keyboard.buttons.afirst()
		telegram_bot_command_keyboard_button.telegram_bot_command = telegram_bot_command_2
		await telegram_bot_command_keyboard_button.asave()

		results: list = await self.send_callback_query(self.handler, '1')
		assert len(results) == 2
		assert results[0]['method'] == 'delete_message'
		assert results[1]['method'] == 'send_message'
		assert results[1]['text'] == telegram_bot_command_2.message_text
