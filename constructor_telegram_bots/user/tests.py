from constructor_telegram_bots.tests import BaseTestCase

from django.http import HttpResponse
from django import urls

from user.models import User

from django.conf import settings


class UserModelsTest(BaseTestCase):
	def test_models(self) -> None:
		user: User = User.objects.filter(
			id=123456789,
			username=None,
			last_login=None,
			confirm_code=None,
			is_superuser=False
		).first()
		self.assertIsNotNone(user)

		self.assertEqual(user.login_url, f'{settings.SITE_DOMAIN}user/login/{user.id}/{user.confirm_code}/')
		self.assertIsNone(user.last_login)
		self.assertIsNotNone(user.confirm_code)

		self.client.get(user.login_url)

		user: User = User.objects.get(id=123456789)
		self.assertIsNotNone(user.last_login)
		self.assertIsNone(user.confirm_code)


class UserViewsTest(BaseTestCase):
	def test_user_login_view(self) -> None:
		login_urls = {
			urls.reverse('user_login', kwargs={'id': 0, 'confirm_code': 0}): 'Не удалось найти пользователя!',
			urls.reverse('user_login', kwargs={'id': 123456789, 'confirm_code': 0}): 'Неверный код подтверждения!',
			self.user.login_url: 'Успешная авторизация',
		}
		
		for login_url in login_urls:
			response: HttpResponse = self.client.get(login_url)
			self.assertEqual(response.status_code, 200)
			self.assertTemplateUsed(response, 'login.html')
			self.assertContains(response, login_urls[login_url])

	def test_user_logout_view(self) -> None:
		url: str = urls.reverse('user_logout')

		self.assertUnauthorizedAccess(url, method='GET')
		
		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'logout.html')


	def test_get_user_telegram_bots_view(self) -> None:
		url: str = urls.reverse('get_user_telegram_bots')

		self.assertUnauthorizedAccess(url)

		response: HttpResponse = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, self.user.get_telegram_bots_as_dict())
