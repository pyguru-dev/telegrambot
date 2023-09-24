from django.test import TestCase, Client
from django.http import HttpResponse
from django import urls
from django.template import defaultfilters as filters

from user.models import User
from telegram_bot.models import *
from telegram_bot.services import database_telegram_bot


class BaseTestCase(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)
		self.user: User = User.objects.create(telegram_id=123456789, first_name='exg1o')
		self.telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=True
		)
		self.telegram_bot_command: TelegramBotCommand = TelegramBotCommand.objects.create(
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
						'row': 1,
						'text': '1',
						'url': None,
					},
					{
						'row': 1,
						'text': '2',
						'url': 'http://example.com/',
					},
				],
			},
			api_request={
				'url': 'http://example.com/',
				'method': 'get',
				'headers': None,
				'data': None,
			},
			database_record={'key': 'value'}
		)
		self.telegram_bot_user: TelegramBotUser = TelegramBotUser.objects.create(
			telegram_bot=self.telegram_bot,
			user_id=123456789,
			full_name='Test user'
		)

class TelegramBotModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot.owner, self.user)
		self.assertEqual(self.telegram_bot.username, '123456789:qwertyuiop_test_telegram_bot')
		self.assertEqual(self.telegram_bot.api_token, '123456789:qwertyuiop')
		self.assertTrue(self.telegram_bot.is_private)
		self.assertFalse(self.telegram_bot.is_running)
		self.assertTrue(self.telegram_bot.is_stopped)

	def test_get_commands_as_dict(self) -> None:
		telegram_bot_commands: list = self.telegram_bot.get_commands_as_dict()
		self.assertListEqual(telegram_bot_commands, [{
			'id': 1,
			'name': 'Test',
			'command': {
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			'image': None,
			'message_text': {
				'mode': 'default',
				'text': 'Test...',
			},
			'keyboard': {
				'mode': 'default',
				'buttons': [
					{
						'id': 1,
						'row': 1,
						'text': '1',
						'url': None,

						'telegram_bot_command_id': None,
						'start_diagram_connector': None,
						'end_diagram_connector' : None,
					},
					{
						'id': 2,
						'row': 1,
						'text': '2',
						'url': 'http://example.com/',

						'telegram_bot_command_id': None,
						'start_diagram_connector': None,
						'end_diagram_connector' : None,
					},
				],
			},
			'api_request': {
				'url': 'http://example.com/',
				'method': 'get',
				'headers': None,
				'data': None,
			},
			'database_record': {'key': 'value'},

			'x': 0,
			'y': 0,
		}])

	def test_get_users_as_dict(self) -> None:
		telegram_bot_users: list = self.telegram_bot.get_users_as_dict()
		self.assertListEqual(telegram_bot_users, [{
			'id': 1,
			'user_id': 123456789,
			'full_name': 'Test user',
			'is_allowed': False,
			'activated_date': f'{filters.date(self.telegram_bot_user.activated_date)} {filters.time(self.telegram_bot_user.activated_date)}',
		}])

	def test_to_dict(self) -> None:
		telegram_bot_as_dict: dict = self.telegram_bot.to_dict()
		self.assertDictEqual(telegram_bot_as_dict, {
			'id': 1,
			'username': '123456789:qwertyuiop_test_telegram_bot',
			'api_token': '123456789:qwertyuiop',
			'is_private': True,
			'is_running': False,
			'is_stopped': True,
			'commands_count': 1,
			'users_count': 1,
			'added_date': f'{filters.date(self.telegram_bot.added_date)} {filters.time(self.telegram_bot.added_date)}',
		})

class TelegramBotCommandModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command.name, 'Test')
		self.assertEqual(self.telegram_bot_command.image, None)
		self.assertDictEqual(self.telegram_bot_command.database_record, {'key': 'value'})
		self.assertEqual(self.telegram_bot_command.x, 0)
		self.assertEqual(self.telegram_bot_command.y, 0)

	def test_get_command(self) -> None:
		telegram_bot_command_command: TelegramBotCommandCommand = self.telegram_bot_command.get_command()
		self.assertEqual(telegram_bot_command_command, self.telegram_bot_command.command)

	def test_get_keyboard(self) -> None:
		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = self.telegram_bot_command.get_keyboard()
		self.assertEqual(telegram_bot_command_keyboard, self.telegram_bot_command.keyboard)

	def test_get_keyboard_as_dict(self) -> None:
		telegram_bot_command_keyboard: dict = self.telegram_bot_command.get_keyboard_as_dict()
		self.assertDictEqual(telegram_bot_command_keyboard, {
			'mode': 'default',
			'buttons': [
				{
					'id': 1,
					'row': 1,
					'text': '1',
					'url': None,

					'telegram_bot_command_id': None,
					'start_diagram_connector': None,
					'end_diagram_connector' : None,
				},
				{
					'id': 2,
					'row': 1,
					'text': '2',
					'url': 'http://example.com/',

					'telegram_bot_command_id': None,
					'start_diagram_connector': None,
					'end_diagram_connector' : None,
				},
			],
		})

	def test_get_api_request(self) -> None:
		telegram_bot_command_api_request: TelegramBotCommandApiRequest = self.telegram_bot_command.get_api_request()
		self.assertEqual(telegram_bot_command_api_request, self.telegram_bot_command.api_request)

	def test_to_dict(self) -> None:
		telegram_bot_command: dict = self.telegram_bot_command.to_dict()
		self.assertDictEqual(telegram_bot_command, {
			'id': 1,
			'name': 'Test',
			'command': {
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			'image': None,
			'message_text': {
				'mode': 'default',
				'text': 'Test...',
			},
			'keyboard': {
				'mode': 'default',
				'buttons': [
					{
						'id': 1,
						'row': 1,
						'text': '1',
						'url': None,

						'telegram_bot_command_id': None,
						'start_diagram_connector': None,
						'end_diagram_connector' : None,
					},
					{
						'id': 2,
						'row': 1,
						'text': '2',
						'url': 'http://example.com/',

						'telegram_bot_command_id': None,
						'start_diagram_connector': None,
						'end_diagram_connector' : None,
					},
				],
			},
			'api_request': {
				'url': 'http://example.com/',
				'method': 'get',
				'headers': None,
				'data': None,
			},
			'database_record': {'key': 'value'},

			'x': 0,
			'y': 0,
		})

class TelegramBotCommandCommandModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command.command.text, '/test')
		self.assertFalse(self.telegram_bot_command.command.is_show_in_menu)
		self.assertIsNone(self.telegram_bot_command.command.description)

	def test_to_dict(self) -> None:
		telegram_bot_command_command: dict = self.telegram_bot_command.command.to_dict()
		self.assertDictEqual(telegram_bot_command_command, {
			'text': '/test',
			'is_show_in_menu': False,
			'description': None,
		})

class TelegramBotCommandMessageTextModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command.message_text.mode, 'default')
		self.assertEqual(self.telegram_bot_command.message_text.text, 'Test...')

	def test_to_dict(self) -> None:
		telegram_bot_command_message_text: dict = self.telegram_bot_command.message_text.to_dict()
		self.assertDictEqual(telegram_bot_command_message_text, {
			'mode': 'default',
			'text': 'Test...',
		})

class TelegramBotCommandKeyboardModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command.keyboard.mode, 'default')

	def test_get_buttons_as_dict(self) -> None:
		telegram_bot_command_keyboard_buttons: list = self.telegram_bot_command.keyboard.get_buttons_as_dict()
		self.assertListEqual(telegram_bot_command_keyboard_buttons, [
			{
				'id': 1,
				'row': 1,
				'text': '1',
				'url': None,

				'telegram_bot_command_id': None,
				'start_diagram_connector': None,
				'end_diagram_connector' : None,
			},
			{
				'id': 2,
				'row': 1,
				'text': '2',
				'url': 'http://example.com/',

				'telegram_bot_command_id': None,
				'start_diagram_connector': None,
				'end_diagram_connector' : None,
			},
		])

	def test_to_dict(self) -> None:
		telegram_bot_command_keyboard: dict = self.telegram_bot_command.keyboard.to_dict()
		self.assertDictEqual(telegram_bot_command_keyboard, {
			'mode': 'default',
			'buttons': [
				{
					'id': 1,
					'row': 1,
					'text': '1',
					'url': None,

					'telegram_bot_command_id': None,
					'start_diagram_connector': None,
					'end_diagram_connector' : None,
				},
				{
					'id': 2,
					'row': 1,
					'text': '2',
					'url': 'http://example.com/',

					'telegram_bot_command_id': None,
					'start_diagram_connector': None,
					'end_diagram_connector' : None,
				},
			],
		})

class TelegramBotCommandKeyboardButtonModelTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton = self.telegram_bot_command.keyboard.buttons.all()[0]

	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command_keyboard_button.row, 1)
		self.assertEqual(self.telegram_bot_command_keyboard_button.text, '1')
		self.assertIsNone(self.telegram_bot_command_keyboard_button.url)
		self.assertIsNone(self.telegram_bot_command_keyboard_button.telegram_bot_command)
		self.assertIsNone(self.telegram_bot_command_keyboard_button.start_diagram_connector)
		self.assertIsNone(self.telegram_bot_command_keyboard_button.end_diagram_connector)

	def test_to_dict(self) -> None:
		telegram_bot_command_keyboard_button: dict = self.telegram_bot_command_keyboard_button.to_dict()
		self.assertDictEqual(telegram_bot_command_keyboard_button, {
			'id': 1,
			'row': 1,
			'text': '1',
			'url': None,

			'telegram_bot_command_id': None,
			'start_diagram_connector': None,
			'end_diagram_connector' : None,
		})

class TelegramBotCommandApiRequestModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command.api_request.url, 'http://example.com/')
		self.assertEqual(self.telegram_bot_command.api_request.method, 'get')
		self.assertIsNone(self.telegram_bot_command.api_request.headers)
		self.assertIsNone(self.telegram_bot_command.api_request.data)

	def test_to_dict(self) -> None:
		telegram_bot_command_api_request: dict = self.telegram_bot_command.api_request.to_dict()
		self.assertDictEqual(telegram_bot_command_api_request, {
			'url': 'http://example.com/',
			'method': 'get',
			'headers': None,
			'data': None,
		})

class TelegramBotUserModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_user.user_id, 123456789)
		self.assertEqual(self.telegram_bot_user.full_name, 'Test user')
		self.assertEqual(self.telegram_bot_user.is_allowed, False)

	def test_to_dict(self) -> None:
		telegram_bot_user: dict = self.telegram_bot_user.to_dict()
		self.assertDictEqual(telegram_bot_user, {
			'id': 1,
			'user_id': 123456789,
			'full_name': 'Test user',
			'is_allowed': False,
			'activated_date': f'{filters.date(self.telegram_bot_user.activated_date)} {filters.time(self.telegram_bot_user.activated_date)}',
		})

class TelegramBotsViewTests(BaseTestCase):
	url: str = urls.reverse('telegram_bots')

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(
			self.url,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': '',
				'is_private': False,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': '123456789:qwertyuiop',
				'is_private': False,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.post(
			self.url,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': '123456789:dwawdadwa',
				'is_private': False,
			}
		)
		self.assertEqual(response.status_code, 200)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, self.user.get_telegram_bots_as_dict())

class TelegramBotViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('telegram_bot', kwargs={'telegram_bot_id': 0})

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.patch(
			self.url_2,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': None,
				'is_private': None,
			}
		)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': None,
				'is_private': None,
			}
		)
		self.assertEqual(response.status_code, 500)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': '',
				'is_private': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': '123456789:qwertyuiop',
				'is_private': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': '123456789:dwawdadwa',
				'is_private': None,
			}
		)
		self.assertEqual(response.status_code, 200)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': None,
				'is_private': False,
			}
		)
		self.assertEqual(response.status_code, 200)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': None,
				'is_private': True,
			}
		)
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.get(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, self.telegram_bot.to_dict())

class StartOrStopTelegramBotViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('start_or_stop_telegram_bot', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('start_or_stop_telegram_bot', kwargs={'telegram_bot_id': 0})

	def test_start_or_stop_telegram_bot_view(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)

class UpdateTelegramBotDiagramCurrentScaleViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('update_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('update_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': 0})

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.patch(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={'diagram_current_scale': 0.8}
		)
		self.assertEqual(response.status_code, 200)

class TelegramBotCommandsViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_commands', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('telegram_bot_commands', kwargs={'telegram_bot_id': 0})

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': '',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': '',
				},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': {
					'text': '',
					'is_show_in_menu': False,
					'description': None
				},
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': {
					'text': '/start',
					'is_show_in_menu': True,
					'description': ''
				},
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': '',
				},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': None,
							'row': None,
							'text': '',
							'url': None,
						},
					],
				},
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': None,
							'row': None,
							'text': '1',
							'url': '',
						},
					],
				},
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': None,
							'row': None,
							'text': '1',
							'url': '-',
						},
					],
				},
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': {
					'url': '',
					'method': 'get',
					'headers': None,
					'data': None,
				},
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': {
					'url': 'test',
					'method': 'get',
					'headers': None,
					'data': None,
				},
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 200)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.get(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, self.telegram_bot.get_commands_as_dict(escape=True))

class TelegramBotCommandViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_command', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': self.telegram_bot_command.id,
		})
		self.url_2: str = urls.reverse('telegram_bot_command', kwargs={
			'telegram_bot_id': 0,
			'telegram_bot_command_id': self.telegram_bot_command.id,
		})
		self.url_3: str = urls.reverse('telegram_bot_command', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': 0,
		})

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.patch(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': '',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': '',
				},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': {
					'text': '',
					'is_show_in_menu': False,
					'description': None,
				},
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': {
					'text': '/start',
					'is_show_in_menu': True,
					'description': '',
				},
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': '1',
							'row': None,
							'text': '',
							'url': None,
						},
					],
				},
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': '1',
							'row': None,
							'text': '1',
							'url': '',
						},
					],
				},
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': '1',
							'row': None,
							'text': '1',
							'url': '-',
						},
					],
				},
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': {
					'url': '',
					'method': 'get',
					'headers': None,
					'data': None,
				},
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': {
					'url': 'test',
					'method': 'get',
					'headers': None,
					'data': None,
				},
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {
					'mode': 'default',
					'text': 'Test...',
				},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.get(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.get(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, self.telegram_bot_command.to_dict())

class UpdateTelegramBotCommandPositionViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('update_telegram_bot_command_position', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': self.telegram_bot_command.id,
		})
		self.url_2: str = urls.reverse('update_telegram_bot_command_position', kwargs={
			'telegram_bot_id': 0,
			'telegram_bot_command_id': self.telegram_bot_command.id,
		})
		self.url_3: str = urls.reverse('update_telegram_bot_command_position', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': 0,
		})

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.patch(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'},)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'x': 123,
				'y': 321,
			}
		)
		self.assertEqual(response.status_code, 200)

class TelegramBotCommandKeyboardButtonTelegramBotCommandViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		telegram_bot_command_keyboard_button_id: int = self.telegram_bot_command.keyboard.buttons.all()[0].id

		self.url_1: str = urls.reverse('telegram_bot_command_keyboard_button_telegram_bot_command', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': self.telegram_bot_command.id,
			'telegram_bot_command_keyboard_button_id': telegram_bot_command_keyboard_button_id,
		})
		self.url_2: str = urls.reverse('telegram_bot_command_keyboard_button_telegram_bot_command', kwargs={
			'telegram_bot_id': 0,
			'telegram_bot_command_id': self.telegram_bot_command.id,
			'telegram_bot_command_keyboard_button_id': telegram_bot_command_keyboard_button_id,
		})
		self.url_3: str = urls.reverse('telegram_bot_command_keyboard_button_telegram_bot_command', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': 0,
			'telegram_bot_command_keyboard_button_id': telegram_bot_command_keyboard_button_id,
		})
		self.url_4: str = urls.reverse('telegram_bot_command_keyboard_button_telegram_bot_command', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': self.telegram_bot_command.id,
			'telegram_bot_command_keyboard_button_id': 0,
		})

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(self.url_4, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(
			self.url_3,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'telegram_bot_command_id': 0,
				'start_diagram_connector': 'test',
				'end_diagram_connector': 'test',
			}
		)
		self.assertEqual(response.status_code, 404)

		telegram_bot_command: TelegramBotCommand = TelegramBotCommand.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test',
			command=None,
			image=None,
			message_text={
				'mode': 'default',
				'text': 'Test...',
			},
			keyboard = None,
			api_request = None,
			database_record = None
		)

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'telegram_bot_command_id': telegram_bot_command.id,
				'start_diagram_connector': 'test',
				'end_diagram_connector': 'test',
			}
		)
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_4, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)

class TelegramBotUsersViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_users', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('telegram_bot_users', kwargs={'telegram_bot_id': 0})

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.get(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, self.telegram_bot.get_users_as_dict())

class TelegramBotUserViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_user', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_user_id': self.telegram_bot_user.id,
		})
		self.url_2: str = urls.reverse('telegram_bot_user', kwargs={
			'telegram_bot_id': 0,
			'telegram_bot_user_id': self.telegram_bot_user.id,
		})
		self.url_3: str = urls.reverse('telegram_bot_user', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_user_id': 0,
		})

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)

class TelegramBotAllowedUserViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_allowed_user', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_user_id': self.telegram_bot_user.id,
		})
		self.url_2: str = urls.reverse('telegram_bot_allowed_user', kwargs={
			'telegram_bot_id': 0,
			'telegram_bot_user_id': self.telegram_bot_user.id,
		})
		self.url_3: str = urls.reverse('telegram_bot_allowed_user', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_user_id': 0,
		})

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)

class TelegramBotDatabeseRecordsViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_databese_records', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('telegram_bot_databese_records', kwargs={'telegram_bot_id': 0})

	def tearDown(self) -> None:
		database_telegram_bot.delete_collection(self.telegram_bot)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={'record': {'key': 'value'}})
		self.assertEqual(response.status_code, 200)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)

		database_telegram_bot.insert_record(self.telegram_bot, {'key': 'value'})

		response: HttpResponse = self.client.get(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, [{'_id': 1, 'key': 'value'}])

class TelegramBotDatabeseRecordViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_databese_record', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'record_id': 1,
		})
		self.url_2: str = urls.reverse('telegram_bot_databese_record', kwargs={
			'telegram_bot_id': 0,
			'record_id': 0,
		})
		self.url_3: str = urls.reverse('telegram_bot_databese_record', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'record_id': 0,
		})

	def tearDown(self) -> None:
		database_telegram_bot.delete_collection(self.telegram_bot)

	def test_patch_method(self) -> None:
		# Надо дописать
		pass

	def test_delete_method(self) -> None:
		# Надо дописать
		pass
