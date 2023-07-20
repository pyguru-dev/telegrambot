from django.test import TestCase, Client
from django.http import HttpResponse
from django import urls


class InstructionViewsTests(TestCase):
	def setUp(self) -> None:
		self.client = Client()

	def test_instruction_view(self) -> None:
		url: str = urls.reverse('instruction')
		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'instruction.html')
