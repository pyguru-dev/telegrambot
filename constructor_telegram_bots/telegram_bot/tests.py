from constructor_telegram_bots.tests import BaseTestCase

from django import urls
from django.template import defaultfilters as filters

from telegram_bot.models import TelegramBot


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
				'is_running': False,
				'is_stopped': True,
				'commands_count': 1,
				'users_count': 1,
				'date_added': f'{filters.date(self.telegram_bot.date_added)} {filters.time(self.telegram_bot.date_added)}',
			}
		)


class TelegramBotViewsTest(BaseTestCase):
	def test_add_telegram_bot_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('add_telegram_bot'),
				'data': {
					'api_token': '123456789:qwertyuiop',
					'is_private': True,
				},
				'response': {
					'message': 'Вы уже используете этот API-токен Telegram бота на сайте!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('add_telegram_bot'),
				'data': {
					'api_token': None,
					'is_private': None,
				},
				'response': {
					'message': 'В тело запроса передан неверный тип данных!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('add_telegram_bot'),
				'data': {
					'api_token': '123456789:dwawdadwa',
					'is_private': True,
				},
				'response': {
					'message': 'Вы успешно добавили Telegram бота.',
					'level': 'success',
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)

	def test_edit_telegram_bot_api_token_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('edit_telegram_bot_api_token', kwargs={'telegram_bot_id': 0}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('edit_telegram_bot_api_token', kwargs={'telegram_bot_id': 1}),
				'data': {
					'api_token': None,
				},
				'response': {
					'message': 'В тело запроса передан неверный тип данных!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('edit_telegram_bot_api_token', kwargs={'telegram_bot_id': 1}),
				'data': {
					'api_token': '123456789:qwertyuiop',
				},
				'response': {
					'message': 'Вы уже используете этот API-токен Telegram бота на сайте!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('edit_telegram_bot_api_token', kwargs={'telegram_bot_id': 1}),
				'data': {
					'api_token': '123456789:dwawdadwa',
				},
				'response': {
					'message': 'Вы успешно изменили API-токен Telegram бота.',
					'level': 'success',
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)

	def test_edit_telegram_bot_private_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('edit_telegram_bot_private', kwargs={'telegram_bot_id': 0}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('edit_telegram_bot_private', kwargs={'telegram_bot_id': 1}),
				'data': {
					'is_private': None,
				},
				'response': {
					'message': 'В тело запроса передан неверный тип данных!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('edit_telegram_bot_private', kwargs={'telegram_bot_id': 1}),
				'data': {
					'is_private': False,
				},
				'response': {
					'message': 'Вы успешно сделали Telegram бота не приватным.',
					'level': 'success',
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)

	def test_delete_telegram_bot_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('delete_telegram_bot', kwargs={'telegram_bot_id': 0}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('delete_telegram_bot', kwargs={'telegram_bot_id': 1}),
				'response': {
					'message': 'Вы успешно удалили Telegram бота.',
					'level': 'success',
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)


	def test_get_telegram_bot_data_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('get_telegram_bot_data', kwargs={'telegram_bot_id': 0}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('get_telegram_bot_data', kwargs={'telegram_bot_id': 1}),
				'response': self.telegram_bot.to_dict(),
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)


	def test_add_telegram_bot_command_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('add_telegram_bot_command', kwargs={'telegram_bot_id': 0}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('add_telegram_bot_command', kwargs={'telegram_bot_id': 1}),
				'data': {
					'image': None,
					'name': None,
					'command': None,
					'message_text': None,
					'keyboard': None,
					'api_request': None,
				},
				'response': {
					'message': 'В тело запроса передан неверный тип данных!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('add_telegram_bot_command', kwargs={'telegram_bot_id': 1}),
				'data': {
					'image': 'null',
					'name': 'Стартовая команда',
					'command': None,
					'message_text': 'Привет!',
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
				},
				'response': {
					'message': 'Введите правильный URL-адрес!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('add_telegram_bot_command', kwargs={'telegram_bot_id': 1}),
				'data': {
					'image': 'null',
					'name': 'Стартовая команда',
					'command': None,
					'message_text': 'Привет!',
					'keyboard': None,
					'api_request': {
						'url': '-',
						'data': '',
					},
				},
				'response': {
					'message': 'Введите правильный URL-адрес!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('add_telegram_bot_command', kwargs={'telegram_bot_id': 1}),
				'data': {
					'image': 'null',
					'name': 'Стартовая команда',
					'command': None,
					'message_text': 'Привет!',
					'keyboard': None,
					'api_request': None,
				},
				'response': {
					'message': 'Вы успешно добавили команду Telegram боту.',
					'level': 'success',
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)

	def test_edit_telegram_bot_command_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('edit_telegram_bot_command', kwargs={'telegram_bot_id': 0, 'telegram_bot_command_id': 1}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('edit_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 0}),
				'response': {
					'message': 'Команда Telegram бота не найдена!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('edit_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
				'data': {
					'image': None,
					'name': None,
					'command': None,
					'message_text': None,
					'keyboard': None,
					'api_request': None,
				},
				'response': {
					'message': 'В тело запроса передан неверный тип данных!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('edit_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
				'data': {
					'image': 'null',
					'name': 'Стартовая команда',
					'command': None,
					'message_text': 'Привет!',
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
				},
				'response': {
					'message': 'Введите правильный URL-адрес!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('edit_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
				'data': {
					'image': 'null',
					'name': 'Стартовая команда',
					'command': None,
					'message_text': 'Привет!',
					'keyboard': None,
					'api_request': {
						'url': '-',
						'data': '',
					},
				},
				'response': {
					'message': 'Введите правильный URL-адрес!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('edit_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
				'data': {
					'image': 'not_edited',
					'name': 'Стартовая команда',
					'command': '/start',
					'message_text': 'Привет!',
					'keyboard': None,
					'api_request': None,
				},
				'response': {
					'message': 'Вы успешно изменили команду Telegram бота.',
					'level': 'success',
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)

	def test_delete_telegram_bot_command_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('delete_telegram_bot_command', kwargs={'telegram_bot_id': 0, 'telegram_bot_command_id': 1}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('delete_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 0}),
				'response': {
					'message': 'Команда Telegram бота не найдена!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('delete_telegram_bot_command', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
				'response': {
					'message': 'Вы успешно удалили команду Telegram бота.',
					'level': 'success',
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)


	def test_get_telegram_bot_command_data_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('get_telegram_bot_command_data', kwargs={'telegram_bot_id': 0, 'telegram_bot_command_id': 1}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('get_telegram_bot_command_data', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 0}),
				'response': {
					'message': 'Команда Telegram бота не найдена!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('get_telegram_bot_command_data', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
				'response': self.telegram_bot_command.to_dict(),
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)


	def test_add_allowed_user_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('add_allowed_user', kwargs={'telegram_bot_id': 0, 'telegram_bot_user_id': 1}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('add_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 0}),
				'response': {
					'message': 'Пользователь Telegram бота не найдена!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('add_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1}),
				'response': {
					'message': 'Вы успешно добавили пользователя в список разрешённых пользователей Telegram бота.',
					'level': 'success',
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)

	def test_delete_allowed_user_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('delete_allowed_user', kwargs={'telegram_bot_id': 0, 'telegram_bot_user_id': 1}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('delete_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 0}),
				'response': {
					'message': 'Пользователь Telegram бота не найдена!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('delete_allowed_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1}),
				'response': {
					'message': 'Вы успешно удалили пользователя из списка разрешённых пользователей Telegram бота.',
					'level': 'success',
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)

	def test_delete_telegram_bot_user_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('delete_telegram_bot_user', kwargs={'telegram_bot_id': 0, 'telegram_bot_user_id': 1}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('delete_telegram_bot_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 0}),
				'response': {
					'message': 'Пользователь Telegram бота не найдена!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('delete_telegram_bot_user', kwargs={'telegram_bot_id': 1, 'telegram_bot_user_id': 1}),
				'response': {
					'message': 'Вы успешно удалили пользователя Telegram бота.',
					'level': 'success',
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)


	def test_save_telegram_bot_diagram_current_scale(self) -> None:
		tests = [
			{
				'url': urls.reverse('save_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': 0}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('save_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': 1}),
				'data': {
					'diagram_current_scale': None,
				},
				'response': {
					'message': 'В тело запроса передан неверный тип данных!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('save_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': 1}),
				'data': {
					'diagram_current_scale': 1.0,
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)

	def test_save_telegram_bot_command_position(self) -> None:
		tests = [
			{
				'url': urls.reverse('save_telegram_bot_command_position', kwargs={'telegram_bot_id': 0, 'telegram_bot_command_id': 1}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('save_telegram_bot_command_position', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 0}),
				'response': {
					'message': 'Команда Telegram бота не найдена!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('save_telegram_bot_command_position', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
				'data': {
					'x': None,
					'y': None,
				},
				'response': {
					'message': 'В тело запроса передан неверный тип данных!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('save_telegram_bot_command_position', kwargs={'telegram_bot_id': 1, 'telegram_bot_command_id': 1}),
				'data': {
					'x': 10,
					'y': 50,
				},
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)


	def test_get_telegram_bot_commands_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('get_telegram_bot_commands', kwargs={'telegram_bot_id': 0}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('get_telegram_bot_commands', kwargs={'telegram_bot_id': 1}),
				'response': self.telegram_bot.get_commands_as_dict(),
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)

	def test_get_telegram_bot_users_view(self) -> None:
		tests = [
			{
				'url': urls.reverse('get_telegram_bot_users', kwargs={'telegram_bot_id': 0}),
				'response': {
					'message': 'Telegram бот не найден!',
					'level': 'danger',
				},
			},
			{
				'url': urls.reverse('get_telegram_bot_users', kwargs={'telegram_bot_id': 1}),
				'response': self.telegram_bot.get_users_as_dict(),
			},
		]

		self.assertUnauthorizedAccess(tests[-1]['url'])
		self.assertTests(tests)
