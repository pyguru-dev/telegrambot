from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
from django.contrib.auth.models import User, Group
import global_decorators as GlobalDecorators

# Create your views here.
@GlobalDecorators.get_navbar_data
def registration_page(request: WSGIRequest, data: dict): # Отрисовка registration.html
	if request.user.is_authenticated == False:
		return render(request, 'registration.html', data)
	else:
		raise Http404('Сначала выйдите из акканута!')

@csrf_exempt
@GlobalDecorators.check_request_data_items(needs_items=['login', 'email', 'password'])
def register_account(request: WSGIRequest, data: dict): # Регистрация аккаунта
	if request.user.is_authenticated == False:
		login, email, password = data['login'], data['email'], data['password']

		if User.objects.filter(username=login).exists() == False:
			user = User.objects.create_user(login, email, password)
			user.save()

			free_accounts_group = Group.objects.get(name='free_accounts')
			user.groups.add(free_accounts_group)

			with open('static/images/user.png', 'rb') as file:
				content = file.read()
			with open(f'static/users_icons/{user.id}.png', 'wb') as file:
				file.write(content)

			return HttpResponse('Успешная регистрация.')
		else:
			return HttpResponseBadRequest(f'Login "{login}" уже занят!')
	else:
		raise Http404('Сначала выйдите из акканута!')