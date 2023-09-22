from django.conf import settings


def constructor_telegram_bot_username(*args, **kwargs) -> dict:
    return {'constructor_telegram_bot_username': settings.CONSTRUCTOR_TELEGRAM_BOT_USERNAME}
