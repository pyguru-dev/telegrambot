from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from telegram_bot.models import TelegramBot

import scripts.decorators as Decorators

# Create your views here.
@Decorators.is_auth(render_page=True)
@Decorators.get_user_data
def personal_cabinet(request: WSGIRequest, data: dict):
	return render(request, 'personal_cabinet.html', context=data)

@Decorators.is_auth(render_page=True)
@Decorators.get_user_data
@Decorators.check_telegram_bot_id(render_page=False)
def telegram_bot_menu(request: WSGIRequest, telegram_bot: TelegramBot, data: dict):
	data.update(
		{
			'telegram_bot': {
				'id': telegram_bot.id,
				'name': telegram_bot.name,
				'token': telegram_bot.token,
				'private': telegram_bot.private,
				'is_running': telegram_bot.is_running,
				'users_activated': telegram_bot.telegram_bot_users.count(),
				'commands': telegram_bot.telegram_bot_command.count(),
				'date_added': telegram_bot.date_added,
			},
		}
	)

	return render(request, 'telegram_bot_menu.html', context=data)