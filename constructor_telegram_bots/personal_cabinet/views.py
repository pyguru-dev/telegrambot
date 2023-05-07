from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from telegram_bot.models import TelegramBot

from constructor_telegram_bots.decorators import *


@login_required
def personal_cabinet(request: WSGIRequest) -> HttpResponse:
	return render(request=request, template_name='personal_cabinet/main.html')

@login_required
@check_telegram_bot_id(render_page=True)
def telegram_bot_menu(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	return render(request=request, template_name='telegram_bot_menu/main.html', context={'telegram_bot': telegram_bot})
