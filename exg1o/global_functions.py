from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import Group

def get_navbar_buttons_data(request: WSGIRequest): # Функция для получения данных для NavBar'а 
	if Group.objects.filter(name='free_accounts').exists() == False:
		free_accounts_group = Group.objects.create(name='free_accounts')
		free_accounts_group.save()
	if Group.objects.filter(name='paid_accounts').exists() == False:
		paid_accounts_group = Group.objects.create(name='paid_accounts')
		paid_accounts_group.save()

	if request.user.is_authenticated:
		data = {
			'navbar': {
				'konstruktor_button': 'on'
			},
			'buttons': {
				'button_1': {
					'id': 'profileButtonLink',
					'onclick': f"window.location.href = '/account/view/{request.user.username}/';",
					'text': 'Профиль'
				},
				'button_2': {
					'id': 'signOutButtonLink',
					'onclick': f"signOut('{request.user.username}');",
					'text': 'Выйти'
				},
				'button_3': {
					'id': 'konstruktorButtonLink',
					'onclick': f"window.location.href = '/account/konstruktor/{request.user.username}/';",
					'text': 'Конструктор'
				}
			}
		}
	else:
		data = {
			'navbar': {},
			'buttons': {
				'button_1': {
					'id': 'authorizationButtonLink',
					'onclick': "window.location.href = '/authorization/';",
					'text': 'Авторизация'
				},
				'button_2': {
					'id': 'registrationButtonLink',
					'onclick': "window.location.href = '/registration/';",
					'text': 'Регистарция'
				}
			}
		}
	return data