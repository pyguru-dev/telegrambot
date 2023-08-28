from constructor_telegram_bots.tests import BaseTestCase

from django.http import HttpResponse
from django import urls
from django.conf import settings

from .models import User


class UserModelsTest(BaseTestCase):
	def test_models(self) -> None:
		user: User = User.objects.filter(
			id=1,
			telegram_id=123456789,
			first_name='exg1o',
			is_staff=False,
			is_superuser=False,
			confirm_code=None,
			last_login=None
		).first()
		self.assertIsNotNone(user)

		self.assertEqual(user.login_url, f"{settings.SITE_DOMAIN}{urls.reverse('user:login', kwargs={'user_id': user.id, 'confirm_code': user.confirm_code})}")
		self.assertIsNotNone(user.confirm_code)
		self.assertIsNone(user.last_login)

		self.client.get(user.login_url)

		user: User = User.objects.get(id=1)
		self.assertIsNone(user.confirm_code)
		self.assertIsNotNone(user.last_login)

class UserViewsTest(BaseTestCase):
	def test_user_login_view(self) -> None:
		login_urls = {
			urls.reverse('user:login', kwargs={'user_id': 0, 'confirm_code': 1}): 'Не удалось найти пользователя!',
			urls.reverse('user:login', kwargs={'user_id': 1, 'confirm_code': 0}): 'Неверный код подтверждения!',
		}

		for login_url in login_urls:
			response: HttpResponse = self.client.get(login_url)
			self.assertEqual(response.status_code, 200)
			self.assertTemplateUsed(response, 'base_success_or_error.html')
			self.assertContains(response, login_urls[login_url])

		response: HttpResponse = self.client.get(self.user.login_url)
		self.assertEqual(response.status_code, 302)

	def test_user_logout_view(self) -> None:
		url: str = urls.reverse('user:logout')

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 302)
		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'base_success_or_error.html')
