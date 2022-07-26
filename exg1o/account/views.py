from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth import logout
from account.models import AccountIconModel
import global_functions as GlobalFunctions
import global_decorators as GlobalDecorators

# Create your views here.
@GlobalDecorators.if_user_authed
def upgrade_account_page(request: WSGIRequest, username: str): # Отрисовка upgrade_account.html
	data = GlobalFunctions.get_navbar_buttons_data(request)
	return render(request, 'upgrade_account.html', data)

@GlobalDecorators.if_user_authed
def view_profile_page(request: WSGIRequest, username: str): # Отрисовка view_profile.html
	user_icon = AccountIconModel.objects.get(owner=request.user.id)

	data = GlobalFunctions.get_navbar_buttons_data(request)
	data.update(
		{
			'user': {
				'name': username,
				'icon': user_icon.icon,
				'status': 'Бесплатный' if request.user.groups.get().name == 'free_accounts' else 'Платный',
				'date_joined': request.user.date_joined
			}
		}
	)
	return render(request, 'view_profile.html', data)

@csrf_exempt
@GlobalDecorators.if_user_authed
def update_user_icon(request: WSGIRequest, username: str):
	user_icon = AccountIconModel.objects.get(owner=request.user.id)
	user_icon.icon = request.body.decode('UTF-8')
	user_icon.save()

	return HttpResponse('Успешная замена авы.')

@GlobalDecorators.if_user_authed
def sign_out(request: WSGIRequest, username: str): # Выход из аккаунта
	logout(request)
	return redirect('/')