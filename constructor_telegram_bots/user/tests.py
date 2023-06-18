from django.test import TestCase, Client
from django.http import HttpResponse
from django import urls
from django.contrib import messages

from telegram_bot.models import TelegramBot
from user.models import User

from django.conf import settings
import json


class UserModelsTest(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)

	def test_user_model(self) -> None:
		self.assertEqual(User.objects.count(), 0)
		user: User = User.objects.create_user(user_id=123456789)
		self.assertEqual(User.objects.count(), 1)

		self.assertEqual(user.id, 123456789)
		self.assertEqual(user.username, None)
		self.assertEqual(user.password, None)
		self.assertEqual(user.last_login, None)
		self.assertEqual(user.confirm_code, None)
		self.assertEqual(user.is_superuser, False)

		self.assertEqual(user.login_url, f'{settings.SITE_DOMAIN}user/login/{user.id}/{user.confirm_code}/')
		self.assertNotEqual(user.confirm_code, None)

		self.client.get(user.login_url)

		user: User = User.objects.get(id=123456789)
		self.assertEqual(user.confirm_code, None)


class UserViewsTest(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)
		self.user: User = User.objects.create_user(user_id=123456789)

	def test_user_login_view(self) -> None:
		login_urls = {
			urls.reverse('user_login', kwargs={'id': 0, 'confirm_code': 0}): 'Не удалось найти пользователя!',
			urls.reverse('user_login', kwargs={'id': 123456789, 'confirm_code': 0}): 'Неверный код подтверждения!',
			self.user.login_url: 'Успешная авторизация',
		}

		login_urls.items()
		
		for login_url in login_urls:
			response: HttpResponse = self.client.get(login_url)
			self.assertEqual(response.status_code, 200)
			self.assertTemplateUsed(response, 'login.html')
			self.assertContains(response, login_urls[login_url])

		self.user: User = User.objects.get(id=self.user.id)
		self.assertNotEqual(self.user.last_login, None)

	def test_user_logout_view(self) -> None:
		response: HttpResponse = self.client.get(urls.reverse('user_logout'))
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)
		
		response: HttpResponse = self.client.get(urls.reverse('user_logout'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'logout.html')


	def test_get_user_telegram_bots_view(self) -> None:
		response: HttpResponse = self.client.post(urls.reverse('get_user_telegram_bots'))
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)
		
		response: HttpResponse = self.client.post(urls.reverse('get_user_telegram_bots'))
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, '[]')

		telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=True
		)

		response: HttpResponse = self.client.post(urls.reverse('get_user_telegram_bots'))
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(
			response.content,
			json.dumps(
				[
					{
						'id': 1,
						'name': '123456789:qwertyuiop_test_telegram_bot',
						'api_token': '123456789:qwertyuiop',
						'is_running': False,
						'is_stopped': True,
						'commands_count': 0,
						'users_count': 0,
						'date_added': telegram_bot.date_added,
					},
				]
			)
		)
