from constructor_telegram_bots.tests import BaseTestCase

from django.http import HttpResponse
from django import urls


class PersonalCabinetViewsTests(BaseTestCase):
	def test_personal_cabinet_view(self) -> None:
		url: str = urls.reverse('personal_cabinet')

		self.assertUnauthorizedAccess(url, method='GET')

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'personal_cabinet/main.html')

	def test_telegram_bot_menu_view(self) -> None:
		url_1: str = urls.reverse('telegram_bot_menu', kwargs={'telegram_bot_id': 1})

		self.assertUnauthorizedAccess(url_1, method='GET')

		url_2: str = urls.reverse('telegram_bot_menu', kwargs={'telegram_bot_id': 0})
		response: HttpResponse = self.client.get(url_2)
		self.assertJSONEqual(
			response.content,
			{
				'message': 'Telegram бот не найден!',
				'level': 'danger',
			}
		)

		response = self.client.get(url_1)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'telegram_bot_menu/main.html')
