from django.test import TestCase

from aiogram import types

from typing import Any


class CustomTestCase(TestCase):
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

		await handler(message)
		return await self.bot.get_results()

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

		await handler(callback_query)
		return await self.bot.get_results()
