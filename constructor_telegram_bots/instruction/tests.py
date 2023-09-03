from django.test import TestCase
from django.http import HttpResponse
from django import urls

from .models import *


class InstructionSectionModelTests(TestCase):
	def setUp(self) -> None:
		self.instruction_section: InstructionSection = InstructionSection.objects.create(position=1, title='Test', text='Test...')

	def test_fields(self) -> None:
		self.assertEqual(self.instruction_section.position, 1)
		self.assertEqual(self.instruction_section.title, 'Test')
		self.assertEqual(self.instruction_section.text, 'Test...')

class ViewsTests(TestCase):
	def test_instruction_view(self) -> None:
		url: str = urls.reverse('instruction')
		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'instruction.html')
