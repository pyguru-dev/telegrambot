from django.conf import settings

def add_telegram_bot_username(request):
    return {'tg_bot_username': settings.CONSTRUCTOR_TELEGRAM_BOT_USERNAME}
