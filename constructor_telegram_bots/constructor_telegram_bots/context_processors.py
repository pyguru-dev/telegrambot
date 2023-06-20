from django.core.handlers.wsgi import WSGIRequest
from django.conf import settings


def add_constructor_telegram_bot_username(request: WSGIRequest) -> dict:
    return {'constructor_telegram_bot_username': settings.CONSTRUCTOR_TELEGRAM_BOT_USERNAME}
