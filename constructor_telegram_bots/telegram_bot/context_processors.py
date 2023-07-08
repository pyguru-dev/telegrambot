from django.http import HttpRequest

from telegram_bot.models import TelegramBot


def telegram_bots(request: HttpRequest) -> dict:
    return {'telegram_bots': TelegramBot.objects.all()}
