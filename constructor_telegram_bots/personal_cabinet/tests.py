from constructor_telegram_bots.tests import BaseTestCase

from django.http import HttpResponse
from django import urls


class PersonalCabinetViewsTests(BaseTestCase):
	def test_personal_cabinet_view(self) -> None:
		url: str = urls.reverse('personal_cabinet')

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 302)
		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'personal_cabinet.html')
