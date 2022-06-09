from django.contrib import admin
from konstruktor.models import TelegramBotModel, TelegramBotCommandModel

# Register your models here.
admin.site.register(TelegramBotModel)
admin.site.register(TelegramBotCommandModel)