from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth import logout
import global_decorators as GlobalDecorators

# Create your views here.
@GlobalDecorators.if_user_authed
@GlobalDecorators.get_navbar_data
def upgrade_account_page(request: WSGIRequest, username: str, data: dict): # Отрисовка upgrade_account.html
	return render(request, 'upgrade_account.html', data)

@GlobalDecorators.if_user_authed
@GlobalDecorators.get_navbar_data
def view_profile_page(request: WSGIRequest, username: str, data: dict): # Отрисовка view_profile.html
	data.update(
		{
			'user': {
				'id': request.user.id,
				'username': username,
				'status': 'Бесплатный' if request.user.groups.get().name == 'free_accounts' else 'Платный',
				'date_joined': request.user.date_joined,
			},
		},
	)
	return render(request, 'view_profile.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
def update_user_icon(request: WSGIRequest, username: str): # Обновление иконки пользователя
	with open(f'static/users_icons/{request.user.id}.png', 'wb') as user_icon:
		user_icon.write(request.body)

	return HttpResponse('Успешная замена авы.')

@GlobalDecorators.if_user_authed
def sign_out(request: WSGIRequest, username: str): # Выход из аккаунта
	logout(request)
	return redirect('/')