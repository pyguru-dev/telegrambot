from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from telegram_bot.models import TelegramBot

from scripts.decorators import SiteDecorators

@SiteDecorators.is_auth(render_page=True)
@SiteDecorators.get_user_data
def personal_cabinet(request: WSGIRequest, data: dict) -> HttpResponse:
	return render(request, 'personal_cabinet/personal_cabinet.html', context=data)

@SiteDecorators.is_auth(render_page=True)
@SiteDecorators.get_user_data
@SiteDecorators.check_telegram_bot_id(render_page=True)
def telegram_bot_menu(request: WSGIRequest, telegram_bot: TelegramBot, data: dict) -> HttpResponse:
	data.update(
		{
			'telegram_bot': {
				'id': telegram_bot.id,
				'name': telegram_bot.name,
				'token': telegram_bot.token,
				'private': telegram_bot.private,
				'is_running': telegram_bot.is_running,
				'commands_count': telegram_bot.commands.count(),
				'users_count': telegram_bot.users.count(),
				'date_added': telegram_bot.date_added,
			},
		}
	)

	return render(request, 'telegram_bot_menu/telegram_bot_menu.html', context=data)