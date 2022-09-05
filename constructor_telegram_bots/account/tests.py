from django.test import TestCase, Client
from django.contrib.auth.models import Group, User

# Create your tests here.
class KonstruktorTestCase(TestCase):
	def setUP(self):
		self.client = Client(enforce_csrf_checks=True)

	def auth_user(self):
		free_accounts_group = Group.objects.create(name='free_accounts')
		free_accounts_group.save()
		paid_accounts_group = Group.objects.create(name='paid_accounts')
		paid_accounts_group.save()

		user = User.objects.create_user('Test', 'test@gmail.com', 'TestTest')
		user.groups.add(free_accounts_group)
		user.save()

		data = {
			'login': 'Test',
			'password': 'TestTest'
		}
		self.client.post('/authorization/authorize_in_account/', data, content_type='application/json')

	def test_successfully_upgrade_account_page(self):
		self.auth_user()

		response = self.client.get('/account/Test/upgrade/')
		self.assertEqual(response.status_code, 200)

	def test_successfully_view_profile_page(self):
		self.auth_user()

		response = self.client.get('/account/view/Test/')
		self.assertEqual(response.status_code, 200)

	def test_successfully_view_profile_page(self):
		self.auth_user()

		response = self.client.post('/account/sign_out/Test/')
		self.assertEqual(response.status_code, 302)