from django.core.handlers.wsgi import WSGIRequest

def get_navbar_buttons_data(request: WSGIRequest): # Функция для получения данных для NavBar'а 
	if request.user.is_authenticated:
		data = {
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