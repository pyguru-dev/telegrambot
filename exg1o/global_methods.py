from django.core.handlers.wsgi import WSGIRequest

def get_navbar_buttons_data(request: WSGIRequest):
	if request.user.is_authenticated:
		data = {
			'button_1': {
				'link': f'/account/view/{request.user.username}',
				'text': 'Профиль'
			},
			'button_2': {
				'link': '/account/sign_out/',
				'text': 'Выйти'
			}
		}
	else:
		data = {
			'button_1': {
				'link': '/authorization/',
				'text': 'Авторизация'
			},
			'button_2': {
				'link': '/registration/',
				'text': 'Регистарция'
			}
		}
	return data