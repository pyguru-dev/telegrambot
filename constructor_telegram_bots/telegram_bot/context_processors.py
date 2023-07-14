from .models import TelegramBot


def telegram_bots(*args, **kwargs) -> dict:
    return {'telegram_bots': TelegramBot.objects.all()}
