from django.test import TestCase, Client
from django.conf import settings

from telegram_bot.models import TelegramBot
from user.models import User

import json


class UserModelsTest(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)

	def test_user_model(self) -> None:
		self.assertEqual(User.objects.count(), 0)
		user = User.objects.create_user(user_id=123456789)
		self.assertEqual(User.objects.count(), 1)

		self.assertEqual(user.id, 123456789)
		self.assertEqual(user.last_login, None)
		self.assertEqual(user.confirm_code, None)
		self.assertEqual(user.is_superuser, False)
		self.assertEqual(user.is_staff, False)
		self.assertEqual(user.telegram_bots.count(), 0)

		login_url = user.get_login_url()
		self.assertNotEqual(user.confirm_code, None)
		self.assertEqual(login_url, f'{settings.SITE_DOMAIN}user/login/{user.id}/{user.confirm_code}/')

		self.assertEqual(user.telegram_bots.count(), 0)
		TelegramBot.objects.add_telegram_bot(user=user, api_token='123456789:qwertyuiop', is_private=True)
		self.assertEqual(user.telegram_bots.count(), 1)

		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(TelegramBot.objects.count(), 1)
		user.delete()
		self.assertEqual(TelegramBot.objects.count(), 0)
		self.assertEqual(User.objects.count(), 0)


class UserViewsTest(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)
		self.user = User.objects.create_user(user_id=123456789)

	def test_user_login_view(self) -> None:
		login_urls = {
			f'/user/login/0/{self.user.confirm_code}/': 'Не удалось найти пользователя!',
			f'/user/login/{self.user.id}/0/': 'Неверный код подтверждения!',
			self.user.get_login_url(): 'Успешная авторизация',
		}

		login_urls.items()
		
		for login_url in login_urls:
			response = self.client.get(login_url)
			self.assertEqual(response.status_code, 200)
			self.assertTemplateUsed(response, 'login.html')
			self.assertContains(response, login_urls[login_url])

		self.user = User.objects.get(id=self.user.id)
		self.assertEqual(self.user.confirm_code, None)
		self.assertNotEqual(self.user.last_login, None)

	def test_user_logout_view(self) -> None:
		login_url = self.user.get_login_url()
		self.client.get(login_url)

		response = self.client.get('/user/logout/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'logout.html')

	def test_get_user_added_telegram_bots_view(self) -> None:
		login_url = self.user.get_login_url()
		self.client.get(login_url)

		telegram_bot = TelegramBot.objects.add_telegram_bot(user=self.user, api_token='123456789:qwertyuiop', is_private=True)

		response = self.client.post('/user/get-telegram-bots/')
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(
			response.content,
			json.dumps(
				[
					{
						'id': 1,
						'name': '123456789:qwertyuiop_test_telegram_bot',
						'api_token': '123456789:qwertyuiop',
						'commands_count': 0,
						'users_count': 0,
						'date_added': telegram_bot.get_date_added(),
					}
				]
			)
		)
