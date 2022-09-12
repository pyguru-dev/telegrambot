from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User
import global_decorators as GlobalDecorators

# Create your views here.
@GlobalDecorators.get_navbar_data
def main_page(request: WSGIRequest, data: dict): # Отрисовка main.html
	site_users = []
	for user in User.objects.all():
		site_users.append(
			{
				'onclick': f"window.location.href = '/view_site_user_profile/{user.id}/'",
				'username': user.username,
			}
		)
	site_users.reverse()

	if site_users == []:
		site_users.append(
			{
				'onclick': "",
				'username': 'Пользователей сайта ещё нет.',
			}
		)

	data.update(
		{
			'users': site_users,
		}
	)
	return render(request, 'main.html', data)

@GlobalDecorators.get_navbar_data
def view_site_user_profile_page(request: WSGIRequest, other_user_id: int, data: dict): # Отрисовка view_site_user_profile.html
	other_user = User.objects.filter(id=other_user_id)

	if other_user.exists():
		other_user = other_user[0]

		data.update(
			{
				'other_user': {
					'id': other_user.id,
					'username': other_user.username,
					'status': 'Бесплатный' if other_user.groups.get().name == 'free_accounts' else 'Платный',
					'date_joined': other_user.date_joined,
				},
			}
		)
		return render(request, 'view_site_user_profile.html', data)
	else:
		raise Http404(f'Пользователя сайта под ID {other_user_id} не существует!')