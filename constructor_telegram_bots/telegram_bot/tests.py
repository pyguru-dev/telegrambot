from constructor_telegram_bots.tests import BaseTestCase

from django.http import HttpResponse
from django import urls
from django.template import defaultfilters as filters

from .models import TelegramBot, TelegramBotCommand


class TelegramBotModelsTest(BaseTestCase):
	def test_models(self) -> None:
		telegram_bot: TelegramBot = TelegramBot.objects.filter(
			id=1,
			username='123456789:qwertyuiop_test_telegram_bot',
			api_token='123456789:qwertyuiop',
			is_private=True,
			is_running=False,
			is_stopped=True
		).first()
		self.assertIsNotNone(telegram_bot)

		self.assertListEqual(
			telegram_bot.get_commands_as_dict(),
			[
				{
					'id': 1,
					'name': 'Стартовая команда',
					'command': None,
					'image': '',
					'message_text': 'Привет!',
					'keyboard': {
						'type': 'defualt',
						'buttons': [
							{
								'id': 1,
								'row': None,
								'text': '1',
								'url': 'http://example.com/',

								'telegram_bot_command_id': None,
								'start_diagram_connector': None,
								'end_diagram_connector' : None,
							},
							{
								'id': 2,
								'row': None,
								'text': '2',
								'url': None,

								'telegram_bot_command_id': None,
								'start_diagram_connector': None,
								'end_diagram_connector' : None,
							},
						],
					},
					'api_request': None,
					'database_record': None,

					'x': 0,
					'y': 0,
				},
			]
		)

		self.assertListEqual(
			telegram_bot.get_users_as_dict(),
			[
				{
					'id': 1,
					'user_id': 123456789,
					'full_name': 'Test A',
					'is_allowed': False,
					'date_activated': f'{filters.date(self.telegram_bot_user.date_activated)} {filters.time(self.telegram_bot_user.date_activated)}',
				},
			]
		)

		self.assertDictEqual(
			telegram_bot.to_dict(),
			{
				'id': 1,
				'username': '123456789:qwertyuiop_test_telegram_bot',
				'api_token': '123456789:qwertyuiop',
				'is_private': True,
				'is_running': False,
				'is_stopped': True,
				'commands_count': 1,
				'users_count': 1,
				'date_added': f'{filters.date(self.telegram_bot.date_added)} {filters.time(self.telegram_bot.date_added)}',
			}
		)

class TelegramBotsViewTest(BaseTestCase):
	url: str = urls.reverse('telegram_bots')

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url, headers={'Authorization': 'Token ---'})
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(
			self.url,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': None,
				'is_private': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {
			'message': 'В тело запроса передан неверный тип данных!',
			'level': 'danger',
		})

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
		self.assertJSONEqual(response.content, {
			'message':'Введите API-токен Telegram бота!',
			'level': 'danger',
		})

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
		self.assertJSONEqual(response.content, {
			'message': 'Вы уже используете этот API-токен Telegram бота на сайте!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			self.url,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'api_token': '123456789:dwawdadwa',
				'is_private': False,
			}
		)

		telegram_bot: TelegramBot = TelegramBot.objects.get(username='123456789:dwawdadwa_test_telegram_bot')

		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно добавили Telegram бота.',
			'level': 'success',

			'telegram_bot': telegram_bot.to_dict(),
		})

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, self.user.get_telegram_bots_as_dict())

class TelegramBotViewTest(BaseTestCase):
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
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

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
		self.assertJSONEqual(response.content, {
			'message': 'Произошла ошибка, попробуйте ещё раз позже!',
			'level': 'danger',
		})

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
		self.assertJSONEqual(response.content, {
			'message': 'Вы уже используете этот API-токен Telegram бота на сайте!',
			'level': 'danger',
		})

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
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно изменили API-токен Telegram бота.',
			'level': 'success',
		})

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
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно сделали Telegram бота не приватным.',
			'level': 'success',
		})

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
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно сделали Telegram бота приватным.',
			'level': 'success',
		})

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.delete(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно удалили Telegram бота.',
			'level': 'success',
		})

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.get(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, self.telegram_bot.to_dict())

class StartOrStopTelegramBotViewTest(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('start_or_stop_telegram_bot', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('start_or_stop_telegram_bot', kwargs={'telegram_bot_id': 0})

	def test_start_or_stop_telegram_bot_view(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': None,
			'level': 'success',
		})

class SaveTelegramBotDiagramCurrentScaleViewTest(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('save_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('save_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': 0})

	def test_save_telegram_bot_diagram_current_scale_view(self) -> None:
		response: HttpResponse = self.client.patch(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.patch(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={'diagram_current_scale': 0.8}
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': None,
			'level': 'success',
		})

class TelegramBotCommandsViewTest(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_commands', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('telegram_bot_commands', kwargs={'telegram_bot_id': 0})

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': '',
				'message_text': 'Привет!',
				'command': None,
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {
			'message': 'Введите название команде!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Стартовая команда',
				'message_text': '',
				'command': None,
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {
			'message': 'Введите текст сообщения!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Стартовая команда',
				'message_text': 'Привет!',
				'command': '',
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {
			'message': 'Введите команду!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Стартовая команда',
				'message_text': 'Привет!',
				'command': None,
				'keyboard': {
					'type': 'inline',
					'buttons': [
						{
							'row': None,
							'text': 'test1',
							'url': '-',
						},
					],
				},
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {
			'message': 'Введите правильный URL-адрес!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Стартовая команда',
				'message_text': 'Привет!',
				'command': None,
				'keyboard': None,
				'api_request': {
					'url': '-',
					'data': '',
				},
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {
			'message': 'Введите правильный URL-адрес!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Стартовая команда',
				'message_text': 'Привет!',
				'command': None,
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно добавили команду Telegram боту.',
			'level': 'success',
		})

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.get(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, self.telegram_bot.get_commands_as_dict(escape=True))

class TelegramBotCommandViewTest(BaseTestCase):
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
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.patch(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Команда Telegram бота не найдена!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Стартовая команда',
				'message_text': 'Привет!',
				'command': None,
				'keyboard': {
					'type': 'inline',
					'buttons': [
						{
							'row': None,
							'text': 'test1',
							'url': '-',
						},
					],
				},
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {
			'message': 'Введите правильный URL-адрес!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Стартовая команда',
				'message_text': 'Привет!',
				'command': None,
				'keyboard': None,
				'api_request': {
					'url': '-',
					'data': '',
				},
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {
			'message': 'Введите правильный URL-адрес!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Стартовая команда',
				'message_text': 'Привет!',
				'command': None,
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			}
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно изменили команду Telegram бота.',
			'level': 'success',
		})

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.delete(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Команда Telegram бота не найдена!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.delete(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно удалили команду Telegram бота.',
			'level': 'success',
		})

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.get(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Команда Telegram бота не найдена!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.get(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, self.telegram_bot_command.to_dict())

class SaveTelegramBotCommandPositionViewTest(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('save_telegram_bot_command_position', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': self.telegram_bot_command.id,
		})
		self.url_2: str = urls.reverse('save_telegram_bot_command_position', kwargs={
			'telegram_bot_id': 0,
			'telegram_bot_command_id': self.telegram_bot_command.id,
		})
		self.url_3: str = urls.reverse('save_telegram_bot_command_position', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': 0,
		})

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.patch(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'},)
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.patch(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Команда Telegram бота не найдена!',
			'level': 'danger',
		})

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
		self.assertJSONEqual(response.content, {
			'message': None,
			'level': 'success',
		})

class TelegramBotCommandKeyboardButtonTelegramBotCommandViewTest(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		telegram_bot_command_keyboard_button_id: int = self.telegram_bot_command_keyboard.get_buttons_as_dict()[0]['id']

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
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Команда Telegram бота не найдена!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(self.url_4, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Кнопка клавиатуры команды Telegram бота не найдена!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			self.url_3,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'telegram_bot_command_id': 0,
				'start_diagram_connector': '',
				'end_diagram_connector': '',
			}
		)
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Команда Telegram бота не найдена!',
			'level': 'danger',
		})

		telegram_bot_command: TelegramBotCommand = TelegramBotCommand.objects.create(
			telegram_bot=self.telegram_bot,
			name='Стартовая команда 2',
			message_text='Привет!'
		)

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'telegram_bot_command_id': telegram_bot_command.id,
				'start_diagram_connector': '',
				'end_diagram_connector': '',
			}
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': None,
			'level': 'success',
		})

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.delete(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Команда Telegram бота не найдена!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.delete(self.url_4, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Кнопка клавиатуры команды Telegram бота не найдена!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.delete(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': None,
			'level': 'success',
		})

class TelegramBotUsersViewTest(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_users', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('telegram_bot_users', kwargs={'telegram_bot_id': 0})

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.get(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, self.telegram_bot.get_users_as_dict())

class TelegramBotUserViewTest(BaseTestCase):
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
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.delete(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Пользователь Telegram бота не найдена!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.delete(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно удалили пользователя Telegram бота.',
			'level': 'success',
		})

class TelegramBotAllowedUserViewTest(BaseTestCase):
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
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Пользователь Telegram бота не найдена!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно добавили пользователя в список разрешённых пользователей Telegram бота.',
			'level': 'success',
		})

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.delete(self.url_3, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Пользователь Telegram бота не найдена!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.delete(self.url_1, headers={'Authorization': f'Token {self.user.auth_token.key}'})
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно удалили пользователя из списка разрешённых пользователей Telegram бота.',
			'level': 'success',
		})
