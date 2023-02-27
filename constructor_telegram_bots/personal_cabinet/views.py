from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

import scripts.decorators as Decorators

# Create your views here.
@Decorators.get_user_data
@Decorators.is_auth(render_page=True)
def personal_cabinet(request: WSGIRequest, data: dict):
	return render(request, 'personal_cabinet.html', context=data)

@Decorators.get_user_data
@Decorators.is_auth(render_page=True)
def telegram_bot_menu(request: WSGIRequest, telegram_bot_id: int, data: dict):
	return render(request, 'telegram_bot_menu.html', context=data)