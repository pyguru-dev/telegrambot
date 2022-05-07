from django.core.handlers.wsgi import WSGIRequest

def get_navbar_buttons_data(request: WSGIRequest):
	if request.user.is_authenticated:
		data = {
			'button_1': {
				'onclick': f"window.location.href = '/account/view/{request.user.username}';",
				'text': 'Профиль'
			},
			'button_2': {
				'onclick': 'signOut();',
				'text': 'Выйти'
			}
		}
	else:
		data = {
			'button_1': {
				'onclick': "window.location.href = '/authorization/';",
				'text': 'Авторизация'
			},
			'button_2': {
				'onclick': "window.location.href = '/registration/';",
				'text': 'Регистарция'
			}
		}
	return data