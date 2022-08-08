from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User
import global_functions as GlobalFunctions

# Create your views here.
def main_page(request: WSGIRequest): # Отрисовка main.html
	site_users = []
	for user in User.objects.all():
		site_users.append(
			{
				'onclick': f"window.location.href = '/view_site_user_profile/{user.id}/'",
				'username': user.username
			}
		)

	if site_users == []:
		site_users.append(
			{
				'onclick': "",
				'username': 'Пользователей сайта ещё нет.'
			}
		)

	data = GlobalFunctions.get_navbar_buttons_data(request)
	data.update(
		{
			'users': site_users
		}
	)
	return render(request, 'main.html', data)

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

def view_site_user_profile_page(request: WSGIRequest, other_user_id: int): # Отрисовка view_site_user_profile.html
	other_user = User.objects.filter(id=other_user_id)

	if other_user.exists():
		other_user = other_user[0]

		data = GlobalFunctions.get_navbar_buttons_data(request)
		data.update(
			{
				'other_user': {
					'id': other_user.id,
					'username': other_user.username,
					'status': 'Бесплатный' if other_user.groups.get().name == 'free_accounts' else 'Платный',
					'date_joined': other_user.date_joined
				}
			}
		)
		return render(request, 'view_site_user_profile.html', data)
	else:
		raise Http404(f'Пользователя сайта под ID {other_user_id} не существует!')