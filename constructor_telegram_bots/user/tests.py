from django.http import HttpResponse
from django import urls

from constructor_telegram_bots.tests import BaseTestCase

from user.models import User

import json


class UserViewsTest(BaseTestCase):
	def test_user_login_view(self) -> None:
		login_urls = {
			urls.reverse('user_login', kwargs={'id': 0, 'confirm_code': 0}): 'Не удалось найти пользователя!',
			urls.reverse('user_login', kwargs={'id': 123456789, 'confirm_code': 0}): 'Неверный код подтверждения!',
			self.user.login_url: 'Успешная авторизация',
		}
		
		for login_url in login_urls:
			self.assertContains(
				url=login_url,
				text=login_urls[login_url],
				status_code=200	
			)
			self.assertTemplateUsed(
				url=login_url,
				template_name='login.html'
			)

		self.user: User = User.objects.get(id=self.user.id)
		self.assertNotEqual(self.user.last_login, None)

	def test_user_logout_view(self) -> None:
		self.assertUserAccess(url=urls.reverse('user_logout'))
		self.assertTemplateUsed(
			url=urls.reverse('user_logout'),
			template_name='logout.html'
		)

	def test_get_user_telegram_bots_view(self) -> None:
		self.assertUserAccess(url=urls.reverse('get_telegram_bots'))
		self.assertJSONEqual(
			url=urls.reverse('get_telegram_bots'),
			data=[
				{
					'id': 1,
					'name': '123456789:qwertyuiop_test_telegram_bot',
					'api_token': '123456789:qwertyuiop',
					'is_running': False,
					'is_stopped': True,
					'commands_count': 0,
					'users_count': 0,
					'date_added': self.telegram_bot.date_added,
				},
			]
		)
