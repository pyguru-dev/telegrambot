from django.test import TestCase
from django.http import HttpResponse
from django import urls
from django.template import defaultfilters as filters

from user.models import User
from telegram_bot.models import TelegramBot

from .models import *


class BaseTestCase(TestCase):
	def setUp(self) -> None:
		self.user: User = User.objects.create(telegram_id=123456789, first_name='exg1o')
		self.telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=True
		)
		self.plugin: Plugin = Plugin.objects.create(user=self.user, telegram_bot=self.telegram_bot, name='Test', code='def test():\n\tpass')
		self.plugin_log: PluginLog = PluginLog.objects.create(
			user=self.user,
			telegram_bot=self.telegram_bot,
			plugin=self.plugin,
			message='Error :-)',
			level='danger'
		)

class PluginModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.plugin.user, self.user)
		self.assertEqual(self.plugin.telegram_bot, self.telegram_bot)
		self.assertEqual(self.plugin.name, 'Test')
		self.assertEqual(self.plugin.code, 'def test():\n\tpass')
		self.assertFalse(self.plugin.is_checked)
		self.assertIsNotNone(self.plugin.added_date)

	def test_to_dict(self) -> None:
		self.assertDictEqual(self.plugin.to_dict(), {
			'id': 1,
			'name': 'Test',
			'code': 'def test():\n\tpass',
			'is_checked': False,
			'added_date': f'{filters.date(self.plugin.added_date)} {filters.time(self.plugin.added_date)}',
		})

class PluginLogModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.plugin_log.user, self.user)
		self.assertEqual(self.plugin_log.telegram_bot, self.telegram_bot)
		self.assertEqual(self.plugin_log.message, 'Error :-)')
		self.assertEqual(self.plugin_log.level, 'danger')
		self.assertIsNotNone(self.plugin_log.added_date)

	def test_to_dict(self) -> None:
		self.assertDictEqual(self.plugin_log.to_dict(), {
			'plugin_name': 'Test',
			'message': 'Error :-)',
			'level': 'danger',
			'added_date': f'{filters.date(self.plugin_log.added_date)} {filters.time(self.plugin_log.added_date)}',
		})

class PluginsViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('plugins', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('plugins', kwargs={'telegram_bot_id': 0})

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(
			self.url_2,
			headers={'Authorization': f'Token {self.user.auth_token.key}'}
		)
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
				'code': 'def test():\n\tpass',
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {
			'message': 'Введите название плагина!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Тест',
				'code': 'def test():\n\tpass',
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {
			'message': 'Название плагина содержит запрещенные символы!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test',
				'code': 'def test():\n\tpass',
			}
		)
		self.assertEqual(response.status_code, 400)
		self.assertJSONEqual(response.content, {
			'message': 'У вас уже добавлен плагин с таким названием!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'name': 'Test1',
				'code': 'def test():\n\tpass',
			}
		)
		self.assertEqual(response.status_code, 200)

		plugin: Plugin = Plugin.objects.get(id=2)

		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно добавили плагин вашему Telegram боту.',
			'level': 'success',

			'plugin': plugin.to_dict(),
		})

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(
			self.url_2,
			headers={'Authorization': f'Token {self.user.auth_token.key}'}
		)
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.get(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'}
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, [self.plugin.to_dict()])

class PluginViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('plugin', kwargs={'plugin_id': self.plugin.id})
		self.url_2: str = urls.reverse('plugin', kwargs={'plugin_id': 0})

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.patch(
			self.url_2,
			headers={'Authorization': f'Token {self.user.auth_token.key}'}
		)
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Плагин не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={'code': 'def test_():\n\tpass'}
		)
		self.assertEqual(response.status_code, 200)

		self.plugin.refresh_from_db()

		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно обновили плагин вашего Telegram бота.',
			'level': 'success',

			'plugin': self.plugin.to_dict(),
		})

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(
			self.url_2,
			headers={'Authorization': f'Token {self.user.auth_token.key}'}
		)
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Плагин не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.delete(
			self.url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'}
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': 'Вы успешно удалили плагин вашего Telegram бота.',
			'level': 'success',
		})

class ViewsTests(BaseTestCase):
	def test_get_plugins_logs_view(self) -> None:
		url_1: str = urls.reverse('plugins_logs', kwargs={'telegram_bot_id': self.telegram_bot.id})
		url_2: str = urls.reverse('plugins_logs', kwargs={'telegram_bot_id': 0})

		response: HttpResponse = self.client.get(url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(
			url_2,
			headers={'Authorization': f'Token {self.user.auth_token.key}'}
		)
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Telegram бот не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.get(
			url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'}
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, [self.plugin_log.to_dict()])

	def test_add_plugin_log_view(self) -> None:
		url_1: str = urls.reverse('plugin_logs', kwargs={'plugin_id': self.plugin.id})
		url_2: str = urls.reverse('plugin_logs', kwargs={'plugin_id': 0})

		response: HttpResponse = self.client.post(url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(
			url_2,
			headers={'Authorization': f'Token {self.user.auth_token.key}'}
		)
		self.assertEqual(response.status_code, 404)
		self.assertJSONEqual(response.content, {
			'message': 'Плагин не найден!',
			'level': 'danger',
		})

		response: HttpResponse = self.client.post(
			url_1,
			headers={'Authorization': f'Token {self.user.auth_token.key}'},
			content_type='application/json',
			data={
				'message': ':D',
				'level': 'success',
			}
		)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, {
			'message': None,
			'level': 'success',
		})
