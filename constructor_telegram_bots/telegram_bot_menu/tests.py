from constructor_telegram_bots.tests import BaseTestCase

from django.http import HttpResponse
from django import urls


class ViewsTests(BaseTestCase):
	def test_telegram_bot_view(self) -> None:
		url: str = urls.reverse('telegram_bot_menu:telegram_bot', kwargs={'telegram_bot_id': self.telegram_bot.id})

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'telegram_bot.html')

	def test_telegram_bot_users_view(self) -> None:
		url: str = urls.reverse('telegram_bot_menu:telegram_bot_users', kwargs={'telegram_bot_id': self.telegram_bot.id})

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'telegram_bot_users.html')

	def test_telegram_bot_database_view(self) -> None:
		url: str = urls.reverse('telegram_bot_menu:telegram_bot_database', kwargs={'telegram_bot_id': self.telegram_bot.id})

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'telegram_bot_database.html')

	def test_telegram_bot_plugins_view(self) -> None:
		url: str = urls.reverse('telegram_bot_menu:telegram_bot_plugins', kwargs={'telegram_bot_id': self.telegram_bot.id})

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'telegram_bot_plugins.html')

	def test_telegram_bot_constructor_view(self) -> None:
		url: str = urls.reverse('telegram_bot_menu:telegram_bot_constructor', kwargs={'telegram_bot_id': self.telegram_bot.id})

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'telegram_bot_constructor/main.html')
