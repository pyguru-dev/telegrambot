from django.test import TestCase
from django.http import HttpResponse
from django import urls
from django.conf import settings

from .models import User


class BaseTestCase(TestCase):
	def setUp(self) -> None:
		self.user: User = User.objects.create(telegram_id=123456789, first_name='exg1o')

class UserModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.user.telegram_id, 123456789)
		self.assertEqual(self.user.first_name, 'exg1o')
		self.assertFalse(self.user.is_superuser)
		self.assertFalse(self.user.is_staff)
		self.assertIsNone(self.user.confirm_code)
		self.assertIsNone(self.user.last_login)

	def test_login_url(self) -> None:
		self.assertEqual(self.user.login_url, f"{settings.SITE_DOMAIN}{urls.reverse('user:login', kwargs={'user_id': self.user.id, 'confirm_code': self.user.confirm_code})}")
		self.assertIsNotNone(self.user.confirm_code)
		self.assertIsNone(self.user.last_login)

		self.client.get(self.user.login_url)

		self.user.refresh_from_db()
		self.assertIsNone(self.user.confirm_code)
		self.assertIsNotNone(self.user.last_login)

class ViewsTests(BaseTestCase):
	def test_user_login_view(self) -> None:
		login_urls = {
			urls.reverse('user:login', kwargs={
				'user_id': 0,
				'confirm_code': 1,
			}): 'Не удалось найти пользователя!',
			urls.reverse('user:login', kwargs={
				'user_id': 1,
				'confirm_code': 0,
			}): 'Неверный код подтверждения!',
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
