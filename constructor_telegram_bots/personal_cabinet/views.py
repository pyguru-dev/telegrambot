from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from telegram_bot.models import TelegramBot

from scripts.decorators import SiteDecorators


@SiteDecorators.is_auth(render_page=True)
def personal_cabinet(request: WSGIRequest) -> HttpResponse:
	return render(request=request, template_name='personal_cabinet/main.html')

@SiteDecorators.is_auth(render_page=True)
@SiteDecorators.check_telegram_bot_id(render_page=True)
def telegram_bot_menu(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	return render(
		request=request,
		template_name='telegram_bot_menu/main.html',
		context={
			'telegram_bot': {
				'id': telegram_bot.id,
				'name': telegram_bot.name,
				'token': telegram_bot.token,
				'private': telegram_bot.private,
				'is_running': telegram_bot.is_running,
				'date_added': telegram_bot.date_added,
			},
		}
	)
