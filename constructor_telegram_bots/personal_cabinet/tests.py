from django import urls

from constructor_telegram_bots.tests import BaseTestCase


class PersonalCabinetViewsTest(BaseTestCase):
	def test_personal_cabinet_view(self) -> None:
		self.assertUserAccess(url=urls.reverse('personal_cabinet'))
		self.assertTemplateUsed(
			url=urls.reverse('personal_cabinet'),
			template_name='personal_cabinet/main.html'
		)

	def test_telegram_bot_menu_view(self) -> None:
		self.assertUserAccess(url=urls.reverse('telegram_bot_menu', kwargs={'telegram_bot_id': 1}))
		self.assertContains(
			url=urls.reverse('telegram_bot_menu', kwargs={'telegram_bot_id': 0}),
			text='Telegram бот не найден!',
			status_code=400
		)
		self.assertTemplateUsed(
			url=urls.reverse('telegram_bot_menu', kwargs={'telegram_bot_id': 1}),
			template_name='telegram_bot_menu/main.html'
		)
