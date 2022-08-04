from django.test import TestCase, Client
from django.contrib.auth.models import User, Group

# Create your tests here.
class RegistrationTestCase(TestCase):
	def setUp(self):
		self.client = Client(enforce_csrf_checks=True)

	def test_successfully_main_page(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_successfully_view_site_user_profile_page(self):
		free_accounts_group = Group.objects.create(name='free_accounts')
		free_accounts_group.save()

		user = User.objects.create_user('Test', 'test@gmail.com', 'TestTest')
		user.save()

		user.groups.add(free_accounts_group)

		response = self.client.get('/view_site_user_profile/1/')
		self.assertEqual(response.status_code, 200)

	def test_fail_view_site_user_profile_page(self):
		response = self.client.get('/view_site_user_profile/1/')
		self.assertEqual(response.status_code, 404)