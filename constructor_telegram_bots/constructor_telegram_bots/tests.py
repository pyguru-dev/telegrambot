from django.test import TestCase, Client
from django.http import HttpResponse

from user.models import User
from telegram_bot.models import TelegramBot

import json
from typing import Union


class BaseTestCase(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)

		self.user: User = User.objects.create_user(user_id=123456789)
		self.telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=True
		)

	def assertTemplateUsed(self, url: str, template_name: str) -> None:
		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		super().assertTemplateUsed(response, template_name)

	def assertContains(self, url: str, text: str, status_code: int) -> None:
		response: HttpResponse = self.client.get(url)
		super().assertContains(
			response=response,
			text=text,
			status_code=status_code
		)

	def assertUserAccess(self, url: str) -> None:
		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 302)

		self.client.get(self.user.login_url)
	
	def assertJSONEqual(self, url: str, data: Union[list, dict]) -> None:
		response: HttpResponse = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		super().assertJSONEqual(response.content, json.dumps(data))
