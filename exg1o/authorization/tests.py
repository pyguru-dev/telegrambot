from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.
class AuthorizationTestCase(TestCase):
	def setUp(self):
		self.client = Client(enforce_csrf_checks=True)

	def create_test_user(self):
		user = User.objects.create_user('Test', 'test@gmail.com', 'TestTest')
		user.save()

	def post_request(self, data: dict):
		response = self.client.post('/authorization/authorize_in_account/', data, content_type='application/json')
		return response.content.decode('UTF-8')

	def test_authorization_page(self):
		response = self.client.get('/authorization/')
		self.assertEqual(response.status_code, 200)

	def test_successfully_authorize_in_account(self):
		self.create_test_user()

		data = {
			'login': 'Test',
			'password': 'TestTest'
		}
		response_text = self.post_request(data)
		self.assertEqual(response_text, 'Успешная авторизация.')

	def test_fail_authorize_in_account_1(self):
		data = {
			'login': 'Test',
			'password': 'TestTest'
		}

		response_text = self.post_request(data)
		self.assertEqual(response_text, 'Такого пользователя не существует!')

	def test_fail_authorize_in_account_2(self):
		self.create_test_user()

		data = {
			'login': 'Test',
			'password': 'Test'
		}
		response_text = self.post_request(data)
		self.assertEqual(response_text, 'Вы ввели неверный "Password"!')