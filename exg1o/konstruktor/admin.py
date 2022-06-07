from django.contrib import admin
from konstruktor.models import TelegramBot, TelegramBotCommand

# Register your models here.
admin.site.register(TelegramBot)
admin.site.register(TelegramBotCommand)