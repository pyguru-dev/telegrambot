from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from telegram_bot.models import TelegramBot

from scripts.decorators import SiteDecorators

@SiteDecorators.is_auth(render_page=True)
@SiteDecorators.get_global_context
def personal_cabinet(request: WSGIRequest, context: dict) -> HttpResponse:
	return render(request=request, template_name='personal_cabinet/main.html', context=context)

@SiteDecorators.is_auth(render_page=True)
@SiteDecorators.get_global_context
@SiteDecorators.check_telegram_bot_id(render_page=True)
def telegram_bot_menu(request: WSGIRequest, telegram_bot: TelegramBot, context: dict) -> HttpResponse:
	context.update(
		{
			'telegram_bot': {
				'name': telegram_bot.name,
				'token': telegram_bot.token,
				'private': telegram_bot.private,
				'is_running': telegram_bot.is_running,
				'date_added': telegram_bot.date_added,
			},
		}
	)

	return render(request=request, template_name='telegram_bot_menu/main.html', context=context)
