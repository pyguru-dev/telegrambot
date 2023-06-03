from django.test import TestCase, Client
from django import urls

from telegram_bot.models import TelegramBot
from user.models import User


class PersonalCabinetViewsTest(TestCase):
	def setUp(self) -> None:
		self.user = User.objects.create_user(user_id=123456789)

		self.client = Client(enforce_csrf_checks=True)

	def test_personal_cabinet_view(self) -> None:
		response = self.client.get(urls.reverse('personal_cabinet'))
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response = self.client.get(urls.reverse('personal_cabinet'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'personal_cabinet/main.html')

	def test_telegram_bot_menu_view(self) -> None:
		TelegramBot.objects.create(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=True	
		)

		response = self.client.get(urls.reverse('telegram_bot_menu', kwargs={'telegram_bot_id': 1}))
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)

		response = self.client.get(urls.reverse('telegram_bot_menu', kwargs={'telegram_bot_id': 0}))
		self.assertContains(response, 'Telegram бот не найден!', status_code=400)

		response = self.client.get(urls.reverse('telegram_bot_menu', kwargs={'telegram_bot_id': 1}))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'telegram_bot_menu/main.html')
