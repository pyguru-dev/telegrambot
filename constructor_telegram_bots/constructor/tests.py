from django.test import TestCase, Client
from django.contrib.auth.models import Group, User

# Create your tests here.
class KonstruktorTestCase(TestCase):
	def setUP(self):
		self.client = Client(enforce_csrf_checks=True)

	def auth_user(self, user_group='free_accounts'):
		free_accounts_group = Group.objects.create(name='free_accounts')
		free_accounts_group.save()
		paid_accounts_group = Group.objects.create(name='paid_accounts')
		paid_accounts_group.save()

		user = User.objects.create_user('Test', 'test@gmail.com', 'TestTest')
		if user_group == 'free_accounts':
			user.groups.add(free_accounts_group)
		elif user_group == 'paid_accounts':
			user.groups.add(paid_accounts_group)
		user.save()

		data = {
			'login': 'Test',
			'password': 'TestTest'
		}
		self.client.post('/authorization/authorize_in_account/', data, content_type='application/json')

	def test_successfully_main_constructor_page_1(self):
		self.auth_user()

		response = self.client.get('/constructor/Test/')
		self.assertEqual(response.status_code, 200)

	def test_successfully_main_constructor_page_2(self):
		self.auth_user(user_group='paid_accounts')

		response = self.client.get('/constructor/Test/')
		self.assertEqual(response.status_code, 200)

	def test_fail_main_constructor_page(self):
		self.auth_user()

		response = self.client.get('/constructor/Fail/')
		self.assertEqual(response.status_code, 400)

	def test_add_bot_page(self):
		self.auth_user()

		response = self.client.get('/constructor/Test/add_bot/')
		self.assertEqual(response.status_code, 200)

	def test_successfully_delete_bot(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': 'fadadawd'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		data = {
			'bot_id': 1
		}
		response = self.client.post('/constructor/Test/delete_bot/', data, content_type='application/json')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'Успешное удаление бота.')

	def test_fail_delete_bot(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': 'fadadawd'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		data = {
			'bot_id': 10
		}
		response = self.client.post('/constructor/Test/delete_bot/', data, content_type='application/json')
		self.assertEqual(response.status_code, 302)

	def test_successfully_add_bot_1(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': 'fadadawd'
		}
		response = self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'Успешное добавление бота.')

	def test_successfully_add_bot_2(self):
		self.auth_user(user_group='paid_accounts')

		data = {
			'bot_name': 'TestBot',
			'bot_token': 'fadadawd'
		}
		response = self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'Успешное добавление бота.')

	def test_fail_add_bot_1(self):
		self.auth_user()

		data = {
			'bot_name': 'Test1Bot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		data = {
			'bot_name': 'Test2Bot',
			'bot_token': '---'
		}
		response = self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'У вас уже максимальное количество ботов!')

	def test_fail_add_bot_2(self):
		self.auth_user(user_group='paid_accounts')

		for i in range(5):
			data = {
				'bot_name': 'Test1Bot',
				'bot_token': '---'
			}
			self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		data = {
			'bot_name': 'Test2Bot',
			'bot_token': '---'
		}
		response = self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'У вас уже максимальное количество ботов!')

	def test_successfully_view_constructor_bot_page_1(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		response = self.client.get('/constructor/Test/view_bot/1/')
		self.assertEqual(response.status_code, 200)

	def test_successfully_view_constructor_bot_page_2(self):
		self.auth_user(user_group='paid_accounts')

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		response = self.client.get('/constructor/Test/view_bot/1/')
		self.assertEqual(response.status_code, 200)

	def test_fail_view_constructor_bot_page(self):
		self.auth_user()

		response = self.client.get('/constructor/Test/view_bot/10/')
		self.assertEqual(response.status_code, 302)

	def test_successfully_save_bot_settings(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		data = {
			'bot_name': 'EditBotName',
			'bot_token': '---'
		}
		response = self.client.post('/constructor/Test/view_bot/1/save_bot_settings/', data, content_type='application/json')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'Успешное сохрание настроек бота.')

	def test_successfully_clear_log(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		response = self.client.post('/constructor/Test/view_bot/1/clear_log/')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'Успешная очистка логов.')

	def test_successfully_add_command_page(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		response = self.client.get('/constructor/Test/view_bot/1/add_command/')
		self.assertEqual(response.status_code, 200)

	def test_successfully_add_command_1(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		data = {
			'command': '/start',
			'command_answer': 'Привет!'
		}
		response = self.client.post('/constructor/Test/view_bot/1/add_command_/', data, content_type='application/json')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'Успешное добавление команды.')

	def test_successfully_add_command_2(self):
		self.auth_user(user_group='paid_accounts')

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		for i in range(15):
			data = {
				'command': '/start',
				'command_answer': 'Привет!'
			}
			self.client.post('/constructor/Test/view_bot/1/add_command_/', data, content_type='application/json')

		data = {
			'command': '/start',
			'command_answer': 'Привет!'
		}
		response = self.client.post('/constructor/Test/view_bot/1/add_command_/', data, content_type='application/json')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'Успешное добавление команды.')

	def test_fail_add_command(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		for i in range(15):
			data = {
				'command': '/start',
				'command_answer': 'Привет!'
			}
			self.client.post('/constructor/Test/view_bot/1/add_command_/', data, content_type='application/json')

		data = {
			'command': '/start',
			'command_answer': 'Привет!'
		}
		response = self.client.post('/constructor/Test/view_bot/1/add_command_/', data, content_type='application/json')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'У вас уже максимальное количество команд!')

	def test_successfully_view_command_page(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		data = {
			'command': '/start',
			'command_answer': 'Привет!'
		}
		self.client.post('/constructor/Test/view_bot/1/add_command_/', data, content_type='application/json')

		response = self.client.get('/constructor/Test/view_bot/1/view_command/1/')
		self.assertEqual(response.status_code, 200)

	def test_fail_view_command_page(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		response = self.client.get('/constructor/Test/view_bot/1/view_command/1/')
		self.assertEqual(response.status_code, 302)

	def test_successfully_save_command(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		data = {
			'command': '/start',
			'command_answer': 'Привет!'
		}
		self.client.post('/constructor/Test/view_bot/1/add_command_/', data, content_type='application/json')

		data = {
			'command': '/hi',
			'command_answer': 'Привет!'
		}
		response = self.client.post('/constructor/Test/view_bot/1/view_command/1/save_command/', data, content_type='application/json')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'Успешное cохранение команды.')

	def test_successfully_delete_command(self):
		self.auth_user()

		data = {
			'bot_name': 'TestBot',
			'bot_token': '---'
		}
		self.client.post('/constructor/Test/add_bot_/', data, content_type='application/json')

		data = {
			'command': '/start',
			'command_answer': 'Привет!'
		}
		self.client.post('/constructor/Test/view_bot/1/add_command_/', data, content_type='application/json')

		response = self.client.post('/constructor/Test/view_bot/1/view_command/1/delete_command/')
		response_text = response.content.decode('UTF-8')
		self.assertEqual(response_text, 'Успешное удаление команды.')