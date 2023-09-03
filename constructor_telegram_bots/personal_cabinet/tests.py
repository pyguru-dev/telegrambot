from django.test import TestCase, Client
from django.http import HttpResponse
from django import urls

from user.models import User


class ViewsTests(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)
		self.user: User = User.objects.create(telegram_id=123456789, first_name='exg1o')

	def test_personal_cabinet_view(self) -> None:
		url: str = urls.reverse('personal_cabinet')

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'personal_cabinet.html')
