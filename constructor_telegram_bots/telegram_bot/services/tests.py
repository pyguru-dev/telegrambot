from django.test import TestCase

from aiogram import types

from user.models import User
from telegram_bot.models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton
)

from telegram_bot.services.user_telegram_bot import UserTelegramBot
from telegram_bot.services.constructor_telegram_bot import ConstructorTelegramBot

from asgiref.sync import sync_to_async

from typing import Any


class BaseTestCase(TestCase):
	async def send_message(self, handler: Any, text: str) -> list:
		message: types.Message = types.Update(
			**{
				'update_id': 1,
				'message': {
					'message_id': 1,
					'from': {
						'id': 1,
						'first_name': 'test',
						'username': 'test',
						'is_bot': False,
						'language_code': 'ru',
					},
					'chat': {
						'id': 1,
						'first_name': 'test',
						'username': 'test',
						'type': 'private',
					},
					'date': 1,
					'text': text,
				},
			}
		).message

		return await handler(message)

	async def send_callback_query(self, handler: Any, data: str) -> list:
		callback_query: types.CallbackQuery = types.Update(
			**{
				'update_id': 1,
				'callback_query': {
					'id': '1',
					'from': {
						'id': 1,
						'first_name': 'Test',
						'username': 'Test',
						'is_bot': False,
						'language_code': 'ru',
					},
					'message': {
						'message_id': 1,
						'from': {
							'id': 1,
							'first_name': 'Test Telegram Bot',
							'is_bot': True,
							'username': 'test_bot',
						},
						'chat': {
							'id': 1,
							'first_name': 'Test',
							'username': 'Test',
							'type': 'private',
						},
							'date': 1,
							'text': '',
							'reply_markup': {
								'inline_keyboard': [],
							},
					},
					'chat_instance': '1',
					'data': data,
				},
			}
		).callback_query

		return await handler(callback_query)


class UserTelegramBotTests(BaseTestCase):
	def setUp(self) -> None:
		self.user: User = User.objects.create_user(user_id=123456789)
		self.telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=False
		)

		self.user_telegram_bot = UserTelegramBot(telegram_bot=self.telegram_bot)
		self.handler = self.user_telegram_bot.message_and_callback_query_handler

	async def test_send_message(self) -> None:
		assert await self.send_message(self.handler,  'Hello') == None

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


class ConstructorTelegramBotTests(BaseTestCase):
	def setUp(self) -> None:
		self.constructor_telegram_bot = ConstructorTelegramBot()

	async def test_start_command(self):
		results: list = await self.send_message(self.constructor_telegram_bot.start_command, '/start')
		assert len(results) == 1
		assert results[0]['method'] == 'send_message'
		assert results[0]['text'] == f"""\
			Привет, @test!
			Я являюсь Telegram ботом для сайта Constructor Telegram Bots.
			Спасибо за то, что ты с нами ❤️
		""".replace('	', '')

	async def test_login_command(self):
		results: list = await self.send_message(self.constructor_telegram_bot.login_command, '/login')

		user: User = await User.objects.afirst()
		login_url: str = await user.alogin_url

		assert len(results) == 1
		assert results[0]['method'] == 'send_message'
		assert results[0]['text'] == 'Нажмите на кнопку ниже, чтобы авторизоваться на сайте.'
		assert results[0]['reply_markup']['inline_keyboard'][0][0]['text'] == 'Авторизация'
		assert results[0]['reply_markup']['inline_keyboard'][0][0]['url'] == login_url
