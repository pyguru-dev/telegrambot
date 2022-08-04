from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.contrib.auth.models import User
import global_functions as GlobalFunctions

# Create your views here.
def main(request: WSGIRequest): # Отрисовка main.html
	site_users = []
	for user in User.objects.all():
		site_users.append(
			{
				'id': user.id,
				'username': user.username
			}
		)

	data = GlobalFunctions.get_navbar_buttons_data(request)
	data.update(
		{
			'users': site_users
		}
	)
	return render(request, 'main.html', data)