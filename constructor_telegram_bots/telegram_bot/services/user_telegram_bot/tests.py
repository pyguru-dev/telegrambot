from telegram_bot.services.tests import BaseTestCase
from telegram_bot.services.custom_aiogram import CustomBot

from user.models import User
from telegram_bot.models import *

from .telegram_bot import UserTelegramBot

from asgiref.sync import sync_to_async
from functools import wraps
import json


class UserTelegramBotTests(BaseTestCase):
	def setUp(self) -> None:
		self.user: User = User.objects.create(telegram_id=123456789, first_name='exg1o')
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
	async def test_send_command(self) -> None:
		await TelegramBotCommand.objects.acreate(
			telegram_bot=self.telegram_bot,
			name='Test',
			command={
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			image=None,
			message_text={
				'mode': 'default',
				'text': 'Test...',
			},
			keyboard=None,
			api_request=None,
			database_record=None
		)

		result: dict = (await self.send_message(self.handler, '/test'))[0]

		assert result['method'] == 'sendMessage'
		assert result['text'] == 'Test...'

	@setup
	async def test_send_command_with_default_keyboard(self) -> None:
		await TelegramBotCommand.objects.acreate(
			telegram_bot=self.telegram_bot,
			name='Test',
			command={
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			image=None,
			message_text={
				'mode': 'default',
				'text': 'Test...',
			},
			keyboard={
				'mode': 'default',
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
			},
			api_request=None,
			database_record=None
		)

		result: dict = (await self.send_message(self.handler, '/test'))[0]
		result_keyboard: dict = json.loads(result['reply_markup'])['keyboard']

		assert result['method'] == 'sendMessage'
		assert result['text'] == 'Test...'
		assert result_keyboard[0][0]['text'] == '1'
		assert result_keyboard[1][0]['text'] == '2'
		assert result_keyboard[1][1]['text'] == '3'

	@setup
	async def test_send_command_with_inline_keyboard(self) -> None:
		await TelegramBotCommand.objects.acreate(
			telegram_bot=self.telegram_bot,
			name='Test',
			command={
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			image=None,
			message_text={
				'mode': 'default',
				'text': 'Test...',
			},
			keyboard={
				'mode': 'inline',
				'buttons': [
					{
						'row': None,
						'text': '1',
						'url': 'https://example.com/',
					},
				],
			},
			api_request=None,
			database_record=None
		)

		result: dict = (await self.send_message(self.handler, '/test'))[0]
		result_keyboard: dict = json.loads(result['reply_markup'])['inline_keyboard']

		assert result['method'] == 'sendMessage'
		assert result['text'] == 'Test...'
		assert result_keyboard[0][0]['text'] == '1'
		assert result_keyboard[0][0]['url'] == 'https://example.com/'

	@setup
	async def test_click_default_keyboard_button(self) -> None:
		telegram_bot_command_1: TelegramBotCommand = await TelegramBotCommand.objects.acreate(
			telegram_bot=self.telegram_bot,
			name='Test',
			command={
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			image=None,
			message_text={
				'mode': 'default',
				'text': 'Test...',
			},
			keyboard={
				'mode': 'default',
				'buttons': [
					{
						'row': None,
						'text': '1',
						'url': None,
					},
				],
			},
			api_request=None,
			database_record=None
		)
		telegram_bot_command_2: TelegramBotCommand = await TelegramBotCommand.objects.acreate(
			telegram_bot=self.telegram_bot,
			name='Test1',
			command=None,
			image=None,
			message_text={
				'mode': 'default',
				'text': 'Test1...',
			},
			keyboard=None,
			api_request=None,
			database_record=None
		)

		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = await sync_to_async(telegram_bot_command_1.get_keyboard)()
		telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton = await telegram_bot_command_keyboard.buttons.afirst()
		telegram_bot_command_keyboard_button.telegram_bot_command = telegram_bot_command_2
		await telegram_bot_command_keyboard_button.asave()

		result: dict = (await self.send_message(self.handler, '1'))[0]

		assert result['method'] == 'sendMessage'
		assert result['text'] == 'Test1...'

	@setup
	async def test_click_inline_keyboard_button(self) -> None:
		telegram_bot_command_1: TelegramBotCommand = await TelegramBotCommand.objects.acreate(
			telegram_bot=self.telegram_bot,
			name='Test',
			command={
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			image=None,
			message_text={
				'mode': 'default',
				'text': 'Test...',
			},
			keyboard={
				'mode': 'inline',
				'buttons': [
					{
						'row': None,
						'text': '1',
						'url': None,
					},
				],
			},
			api_request=None,
			database_record=None
		)
		telegram_bot_command_2: TelegramBotCommand = await TelegramBotCommand.objects.acreate(
			telegram_bot=self.telegram_bot,
			name='Test1',
			command=None,
			image=None,
			message_text={
				'mode': 'default',
				'text': 'Test1...',
			},
			keyboard=None,
			api_request=None,
			database_record=None
		)

		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = await sync_to_async(telegram_bot_command_1.get_keyboard)()
		telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton = await telegram_bot_command_keyboard.buttons.afirst()
		telegram_bot_command_keyboard_button.telegram_bot_command = telegram_bot_command_2
		await telegram_bot_command_keyboard_button.asave()

		results: list = await self.send_callback_query(self.handler, '1')

		assert results[0]['method'] == 'deleteMessage'
		assert results[1]['method'] == 'sendMessage'
		assert results[1]['text'] == 'Test1...'
