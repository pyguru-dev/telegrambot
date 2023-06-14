from django import urls

from constructor_telegram_bots.tests import BaseTestCase


class HomeViewsTest(BaseTestCase):
	def test_home_view(self) -> None:
		self.assertTemplateUsed(
			url=urls.reverse('home'),
			template_name='home.html'
		)
