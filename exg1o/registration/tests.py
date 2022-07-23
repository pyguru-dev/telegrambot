from django.test import TestCase, Client
from django.contrib.auth.models import Group, User

# Create your tests here.
class RegistrationTestCase(TestCase):
	def setUp(self):
		self.client = Client(enforce_csrf_checks=True)

		free_accounts_group = Group.objects.create(name='free_accounts')
		free_accounts_group.save()
		paid_accounts_group = Group.objects.create(name='paid_accounts')
		paid_accounts_group.save()

	def post_request(self, data: dict):
		response = self.client.post('/registration/register_account/', data, content_type='application/json')
		return response.content.decode('UTF-8')

	def test_registration_page(self):
		response = self.client.get('/registration/')
		self.assertEqual(response.status_code, 200)

	def test_successfully_register_account(self):
		data = {
			'login': 'Test',
			'email': 'test@gmail.com',
			'password': 'TestTest'
		}

		response_text = self.post_request(data)
		self.assertEqual(response_text, 'Успешная регистрация.')

	def test_fail_register_account_1(self):
		data = {
			'login': 'Test',
			'email': 'test@gmail.com',
			'password': 'TestTest'
		}

		user = User.objects.create_user('Test', 'test@gmail.com', 'TestTest')
		user.save()

		response_text = self.post_request(data)
		self.assertEqual(response_text, 'Login "Test" уже занят!')